// Function responsible for loading and managing posts on a profile page
function load_posts_profile(load) {
    // Clear the existing posts
    document.querySelector(".all_posts").innerHTML = '';

    // Get the CSRF token
    const csrfToken = document.querySelector('#csrf_token').value;

    // Fetch posts data based on the provided 'load' parameter
    fetch(`/load_posts/${load}`)
        .then(response => response.json())
        .then(posts => {

            // Update profile information and visibility of sections
            // based on the retrieved posts data
            var profile = document.getElementById("profile_header");
            profile.style.display = 'inline-block';
            var useraccount = document.getElementById("username");

            // Get a reference to the 'Followers' section by its id
            var followersSection = document.getElementById("followers-column");
            var followingSection = document.getElementById("following-column");

            // Set the content of the section to the followers count
            followersSection.innerHTML = posts.count.followers;
            followingSection.innerHTML = posts.count.following;

            const notUserProfile = posts.isCurrentProfile;

            document.querySelector('#followingsection').style.display = posts.isCurrentProfile ? 'none' : 'block';
            document.querySelector('#new_posts').style.display = notUserProfile ? 'none' : 'block';

            if (notUserProfile) {
                document.querySelector("#profile_header").innerText = `${load}'s Posts`;
                document.querySelector("#profile_header").value = load;

                if (load != useraccount.innerHTML) {
                    profile.insertAdjacentElement('afterend', follow_icon);
                }
            } else {
                document.querySelector("#profile_header").innerText = "All Posts";
                const follow_icon = document.querySelector('.follow_icon');
                if (follow_icon) { follow_icon.remove(); }
            }
            // Load new posts
            load_newpage(posts, true);

            /// Append pagination elements after the posts are loaded
            add_pagination(posts, undefined, true);

        })
}

// Function responsible for loading new posts and updating the UI
function load_newpage(postdata, newset) {

    // Clear existing posts and pagination elements if 'newset' is not true
    if (newset != true) {
        const posts = document.querySelectorAll('.post');
        posts.forEach(link => { link.remove(); });
        document.querySelector('[aria-label="Page navigation example"]').remove();
        const page_selection_element = document.querySelectorAll('.page-item');
        page_selection_element.forEach(link => { link.remove(); });
    }
    // Iterate through the retrieved posts data and create post elements
    postdata.data.forEach((element, index) => {
        let line = CreatePostUI(element, postdata.current_user);
        // Append the newly created post elements to the UI
        document.querySelector(".all_posts").innerHTML += line.outerHTML;
        // Update like button icons based on the 'current_user_like' property of each post
        document.querySelector(`#post_${element.id} path:nth-of-type(1)`).setAttribute('d', element.current_user_like ? 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z' : 'm8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z');

    })
}

// Function responsible for loading posts from followed users
function following() {

    // Fetch posts from followed users
    fetch(`/following`)
        .then(response => response.json())
        .then(posts => {

            // Load new posts and append pagination elements
            load_newpage(posts, newset = false);
            add_pagination(posts, posts, true, followinguser = true);
        })
}

// Function responsible for loading child comments for a parent comment
function LoadChildComments(parentID, ChildCommentPage = 1) {
    // Get the parent comment element
    let parentcomment = document.querySelector(`#post_${parentID}`);

    
        // Fetch child comments for the parent comment
        fetch('/loadchildcomments', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: JSON.stringify({
                id: parentID,
                page: ChildCommentPage
            })
        })
            .then(response => response.json())
            .then(posts => {
                const returndata = posts;
                let childcommentDiv = parentcomment.querySelector('.child-comment-container');
                //Removes any Child Comments before loading queiried comment in order to avoid loading duplicate comments since comments are appended to DOM before they are submitted  
                
                posts.ChildCommentData.forEach((element) => {

                    // Update the UI with the retrieved child comments
                    let childcommentDiv = parentcomment.querySelector('.child-comment-container');
                    if (!childcommentDiv) {
                        childcommentDiv = document.createElement('span');
                        childcommentDiv.className = 'child-comment-container';
                        childcommentDiv.append(CreatePostUI(element, posts.current_user, true));
                        parentcomment.append(childcommentDiv);
                    }
                    else {
                        childcommentDiv.append(CreatePostUI(element, posts.current_user, true));
                    }
                    post = childcommentDiv.querySelector(`#post_${element.id}`);
                    change = post.querySelector(`.like_button`);

                });
                //add a "Show More Replies" button if there are more comments to load
                if (returndata.NextPage > 0) {

                    childcommentDiv.append(showMoreReplies(parentID, returndata.NextPage));
                }
            })

    
    
    changeRepliesfunction(`#post_${parentID}`)
}

// Function responsible for posting comments or child comment(comments of posts)
function PostComment() {
    let edit_field = document.querySelector('.edit_field').value;

    // Get the comment content. If childcomment is true that means a comment to a post was created. if false we are editing a post or comment
    fetch(`/postcomment`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: JSON.stringify({
            post_id: removeLetters(current_edit.id),
            post: edit_field
        })
    })
        .then(response => response.json())
        .then(post => {
            //figure out the most efficient and aesthesitic way to render in new comments 
            remove_edit(false, null, post.ChildCommentData.currentprofile);

            let current_post_div = document.querySelector(`#post_${removeLetters(post.ChildCommentData.parentcomment)}`);
            //if childcomment Div already exists you can just append but if it does not create it and add in your new post after searching and populating all other posts. But only perform search if the number of child posts is more than one
            childcommentDiv = current_post_div.querySelector('.child-comment-container');
            if (!childcommentDiv) {
                childcommentDiv = document.createElement('span'); childcommentDiv.className = '.child-comment-container';
            }
            childcommentDiv.append(CreatePostUI(post.ChildCommentData, post.current_user, true));
            current_post_div.append(childcommentDiv);
            current_post_div.querySelector('.reply-text').innerText = `${post.ChildCommentData.ParentRepliesCount} Replies`;

        });
}


function editComment() {
    let edit_field = document.querySelector('.edit_field').value;

    fetch('/editpost', {
        method: 'PUT',
        headers: { 'X-CSRFToken': csrfToken },
        body: JSON.stringify({
            post_id: removeLetters(current_edit.id),
            post: edit_field
        })
    })
        .then(response => response.json())
        .then(post => {
            //Removes the Edit Textfield element
            remove_edit(false, null);
            let current_post_div = document.querySelector(`${current_edit.id}`);
            current_post_div.querySelector('.post_string').innerText = post.update;
            current_edit = { 'id': `#post_${removeLetters(current_edit.id)}`, 'innerhtml': current_post_div.innerHTML };
            current_post_div.querySelector('.reply-text').innerText = `${post.ChildCommentData.ParentRepliesCount} Replies`;
        })
}

function follow() {
    var csrfToken = follow_icon.getAttribute('data-csrf-token');
    username = document.getElementById("profile_header").value;
    fetch(`/follow/${username}`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            id: username
        })
    })
        .then(response => response.json())
        .then(updated_counter => {
            if (updated_counter.followers != true) {
                document.querySelector(`#followers-column`).innerHTML = updated_counter.followers;
            }


        })
}

function create_post() {
    var comment = document.querySelector('#compose-comment').value;

    fetch('/create_post', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            comment: comment
        })
    })
        .then(response => response.json())
        .then(updatepost => {
            document.querySelector('#compose-comment').value = '';
            load_newpage(updatepost, false);
            add_pagination(updatepost, undefined, true);
        })


}

function like_post(id) {
    fetch(`/like_post/${id}`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
        .then(response => response.json())
        .then(like => {
            let counter_element = document.querySelector(`#post_${id}`);

            counter_element.querySelector(`.like-counter`).innerText = like.Newpost.like_count;
            document.querySelector(`#post_${id} path:nth-of-type(1)`).setAttribute('d', like.Newpost.liked ? 'm8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z' : 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z');
        })

}