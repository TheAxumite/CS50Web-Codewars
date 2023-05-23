


let current_edit = '';
function CreateHeart(id, like) {
    // create button element
    var like_button_unlike = document.createElement('button');
    like_button_unlike.className = 'like_button';
    like_button_unlike.style.backgroundColor = ' #23232452';

    like_button_unlike.style.border = 'transparent';


    // create SVG element
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('width', '16');
    svg.setAttribute('height', '16');
    svg.setAttribute('fill', 'currentColor');
    svg.setAttribute('class', 'bi bi-hand-thumbs-up-fill');
    svg.setAttribute('viewBox', '0 0 16 16');

    // create path element
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');

    path.setAttribute('d', like ? 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z' : 'm8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z');


    // append path element to SVG element
    svg.appendChild(path);

    // append SVG element to button element
    like_button_unlike.appendChild(svg);
    like_button_unlike.setAttribute('onclick', `like_post(${id})`);
    like_button_unlike.setAttribute('data-csrf-token', csrfToken);

    return like_button_unlike
}
//button hover listner  for Follow button
const mySVG = document.getElementsByClassName('like_button');
const follow_icon = document.createElement('img');
follow_icon.src = "{% static 'network/follow.png' %}";
follow_icon.className = 'follow_icon';
follow_icon.style.width = '64px';
follow_icon.style.height = '64px';
follow_icon.style.cursor = 'pointer';
follow_icon.style.display = 'inline-block';
const csrfToken = document.querySelector('#csrf_token').value;
follow_icon.setAttribute('data-csrf-token', csrfToken);
//follow button attribute when clicked runs the follow function
follow_icon.setAttribute('onclick', `follow()`);

mySVG.onmouseover = function () {
    this.querySelector('rect').setAttribute('fill', 'white');
};

mySVG.onmouseout = function () {
    this.querySelector('rect').setAttribute('fill', 'blue');
};

follow_icon.onmouseover = function () {
    this.style.height = '74px';
    this.style.width = '74px';
};

follow_icon.onmouseout = function () {
    this.style.height = '64px';
    this.style.width = '64px';
};

export function createNavItem(text, ul) {
    const item = document.createElement('li');
    item.className = 'page-item';
    const link = document.createElement('a');
    link.className = 'page-link';
    link.innerText = text;
    link.addEventListener("click", PageTracker.page_selection);
    item.appendChild(link);
    ul.appendChild(item);
}

function isAlphabet(char) {
    return /^[a-zA-Z]$/.test(char);
}




//visiting the page it should add follow user option
function load_posts_profile(load) {
    document.querySelector(".all_posts").innerHTML = '';
    const csrfToken = document.querySelector('#csrf_token').value;

    fetch(`/load_posts/${load}`)
        .then(response => response.json())
        .then(posts => {

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
            load_newpage(posts, true);

            //appends pagitation html elmemnts after the DOM loads all the posts
            add_pagination(posts, undefined, true);

        })
}
//TODO: Function  need to be modified for child comments a bit. Remove div and append on the Post Div instead
function CreatePostUI(element, CurrentUserData, childcomment = false, ChildCommentPage = 1) {
    let dots = document.createElement("span");
    dots.className = childcomment ? 'child-edit-button' : 'edit_button';
    dots.innerHTML = "⋮";
    dots.setAttribute('onclick', `open_edit(${element.id}, ${childcomment})`);
    dots.dataset.value = "0";
    dots.id = element.id;
    let line = document.createElement('div');
    let time_stamp = document.createElement('span');
    time_stamp.className = "time_stamp";
    time_stamp = element.timestamp;
    let post_user = document.createElement('a');
    post_user.style.color = '#007bff';
    post_user.className = "post_user";
    post_user.style.cursor = 'pointer';
    post_user.style.textDecoration = 'underline';
    post_user.innerHTML = element.user;
    post_user.setAttribute('onclick', `load_posts_profile("${element.user}")`);
    let post = document.createElement('div');
    post.className = 'post_string';
    post.innerHTML = element.post;
    let count_likes = document.createElement('span');
    count_likes.className = 'like-counter';
    count_likes.textContent = element.post_likes;
    line.className = childcomment ? "post-child" : "post";
    line.id = `post_${element.id}`;

    //Create Reply Button 
    let reply = document.createElement('span');
    reply.innerText = 'Reply';
    reply.className = 'reply-button';
    reply.setAttribute('onclick', `create_edit_field(${element.id}, childcomment = true)`)

    //Replies button for viewing all comments
    let replies = document.createElement('div');
    replies.className = 'replies-div';
    replies.dataset.value = '0';
    //Create a span element for containing the 'Replies' string
    let replytext = document.createElement('span');
    replytext.className = 'reply-text';

    replytext.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                            <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                            </svg>`;
    replytext.innerHTML += `<span class = 'reply-text-child'>${element.replies} Replies</span>`;
    replytext.setAttribute('onclick', `LoadChildComments(${element.id}, ${ChildCommentPage})`)
    replies.append(replytext);
    //create child comment Container if the UI being created is for an original
    if (childcomment === false) {
        childcommentDiv = document.createElement('span');
        childcommentDiv.className = 'child-comment-container';
        var rect = replies.getBoundingClientRect();
        childcommentDiv.style.position = "relative";
        childcommentDiv.style.left = (rect.left + 15) + 'px';
    }

    line.append(post_user);
    if (element.user === CurrentUserData) {
        line.append(time_stamp, dots, post, CreateHeart(element.id, element.current_user_like), count_likes, reply, replies, childcomment ? '' : childcommentDiv);
    }
    else {
        line.append(time_stamp, post, CreateHeart(element.id, element.current_user_like), count_likes, reply, replies, childcomment ? '' : childcommentDiv);
    }
    return line;
}



function load_newpage(postdata, newset) {
    if (newset != true) {
        const posts = document.querySelectorAll('.post');
        posts.forEach(link => { link.remove(); });
        document.querySelector('[aria-label="Page navigation example"]').remove();
        const page_selection_element = document.querySelectorAll('.page-item');
        page_selection_element.forEach(link => { link.remove(); });
    }
    postdata.data.forEach((element, index) => {
        let line = CreatePostUI(element, postdata.current_user);
        document.querySelector(".all_posts").innerHTML += line.outerHTML;
        document.querySelector(`#post_${element.id} path:nth-of-type(1)`).setAttribute('d', element.current_user_like ? 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z' : 'm8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z');

    })
}






function item_element(i, ul, following = false) {
    const pageItem = document.createElement('li');
    pageItem.className = 'page-item';
    const pageLink = document.createElement('a');
    pageLink.className = 'page-link .bg-dark';
    pageLink.innerText = i;
    pageLink.dataset.value = following ? 'Following' : null;
    pageLink.addEventListener("click", PageTracker.page_selection);
    pageItem.appendChild(pageLink);
    ul.appendChild(pageItem);
    return { pageItem: pageItem };
}

function createNavItem(text, ul) {
    const item = document.createElement('li');
    item.className = 'page-item';
    const link = document.createElement('a');
    link.className = 'page-link .bg-dark';
    link.innerText = text;
    link.addEventListener("click", PageTracker.page_selection);
    item.appendChild(link);
    ul.appendChild(item);
}

function isAlphabet(char) {
    return /^[a-zA-Z]$/.test(char);
}

class PageTracker {
    // Method to get the last number of set for pagination.
    static LastSet(pagedata, postdata, pageLinks) {
        return (pagedata.next_set === true) ? Math.min(parseInt(pageLinks[pageLinks.length - 2].innerHTML) + 1 + postdata.pages_left,
            parseInt(pageLinks[pageLinks.length - 2].innerHTML) + 5) : (pagedata.previous_set === true)
            ? pagedata.page + 4 :
            pagedata.page <= parseInt(isAlphabet(pageLinks[pageLinks.length - 1].innerHTML[0])
                ? pageLinks[pageLinks.length - 2].innerHTML
                : pageLinks[pageLinks.length - 1].innerHTML)
                ? parseInt(
                    isAlphabet(pageLinks[pageLinks.length - 1].innerHTML[0])
                        ? pageLinks[pageLinks.length - 2].innerHTML :
                        pageLinks[pageLinks.length - 1].innerHTML) :
                pagedata.page + postdata.pages_left + 1
    }

    // Method to get the first number of set for pagination.
    static FirstSet(pagedata, postdata, pageLinks) {

        return (pagedata.next_set === true)
            ? parseInt(pageLinks[pageLinks.length - 2].innerHTML) + 1
            : (pagedata.previous_set === true) ? pagedata.page
                : isAlphabet(pageLinks[0].innerHTML[0]) ? pageLinks[1].innerHTML
                    : pageLinks[0].innerHTML
    }

    static page_selection(event) {
        const page_number = event.target;

        const profileHeader = document.querySelector('#profile_header').innerHTML;

        let load = {
            'page': (page_number.innerHTML === 'Next') ?
                parseInt(page_number.parentElement.previousElementSibling.innerText) + 1 :
                (page_number.innerHTML === 'Previous') ?
                    parseInt(page_number.parentElement.nextElementSibling.innerText) - 5 :
                    parseInt(page_number.innerHTML),
            'next_set': (page_number.innerHTML == 'Next'),
            'previous_set': (page_number.innerHTML == 'Previous'),
            'profile': (profileHeader.slice(-8) === "'s Posts") ? profileHeader.slice(0, -8) : profileHeader
        }
        const jsonString = JSON.stringify(load);
        const encodedData = encodeURIComponent(jsonString);
        fetch(`/load_page/${encodedData}`)
            .then(response => response.json())
            .then(page => { add_pagination(page, load, false) })
    }
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
let previous = 0;
//Function opens the edit button element in this case the element is a 3-dot element
function open_edit(id, childcomment) {
    // Obtain the 3-dot menu element used for accessing the edit options. Its Element ID is linked to the post's primary key (PK) ID in the backend. Initially, the data-value is set to 0, indicating an inactive state.
    const edit_dot = document.getElementById(id);
    // Check if an element with the 'edit_button_div' class already exists
    var existing_edit_div = document.querySelector('.edit_button_div');
    if (existing_edit_div && edit_dot.dataset.value === "1") { existing_edit_div.remove(); edit_dot.dataset.value = 0; return; }

    if (existing_edit_div && edit_dot.dataset.value === "0" && edit_dot.id != previous) { existing_edit_div.remove(); document.getElementById(`${previous}`).dataset.value = 0; }

    // If it exists, remove the existing 'edit_button_div'
    if (edit_dot) {
        if (edit_dot.dataset.value === "0") {
            if (existing_edit_div) { existing_edit_div.remove(); }
            let edit_div = document.createElement("div");
            edit_div.className = 'edit_button_div';
            edit_dot.dataset.value = "1";
            edit_div.innerText = 'Edit';
            edit_div.style.color = 'white';
            edit_div.style.cursor = 'pointer';
            edit_div.setAttribute('onclick', `edit_post(${id}, ${childcomment})`);
            edit_dot.append(edit_div);
            previous = edit_dot.id;
            return;
        }
    }
    return;
}


//used to remove strings only and retrieve post number from a post element
function removeLetters(str) {
    return str.replace(/[^\d]/g, '');
};



function PostComment(childcomment = false) {

    let edit_field = document.querySelector('.edit_field').value;


    fetch(childcomment ? `/postchildcomment(true)` : `/postcomment`, {
        method: childcomment ? 'POST' : 'PUT',
        headers: { 'X-CSRFToken': csrfToken },
        body: JSON.stringify({
            post_id: removeLetters(current_edit.id),
            post: edit_field
        })
    })
        .then(response => response.json())
        .then(post => {

            if (childcomment == false) {
                remove_edit(false, null, post.ChildCommentData.currentprofile);
                let current_post_div = document.querySelector(`${current_edit.id}`);
                current_post_div.querySelector('.post_string').innerText = post.update;
                current_edit = { 'id': `#post_${removeLetters(current_edit.id)}`, 'innerhtml': current_post_div.innerHTML };
                current_post_div.querySelector('.reply-text').innerText = `${post.ChildCommentData.ParentRepliesCount} Replies`;

            }

            else {

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
                console.log(post.ChildCommentData.ParentRepliesCount);
            }
        })
}

function remove_edit(childcomment = false, id = null, currentprofile = null) {
    if (childcomment === true) {
        let previous_post = document.querySelector(`${current_edit.id}`);
        if (previous_post) {
            // Get all children elements of previous_post
            let childcomment = previous_post.querySelector('.child-comment');
            // Check if there are at least two children elements
            if (childcomment) {
                // Get the second-to-last element
                childcomment.remove();
            }
            return;
        }
    }
    let previous_post = document.querySelector(`${current_edit.id}`);
    if (previous_post) {
        previous_post.innerHTML = current_edit.innerhtml;
        if (currentprofile == true || currentprofile == null) {
            let edit_box = document.getElementById(removeLetters(current_edit.id)).firstElementChild;
            if (edit_box) {
                edit_box.remove();
            }
        }
    }
    return;
}


function autoGrow(edit_field) {
    edit_field.style.height = 'auto';
    edit_field.style.height = (edit_field.scrollHeight) + 'px';
}


function onInputHandler() {
    autoGrow(this);
}
function create_edit_field(id, childcomment = false) {

    const post = document.querySelector(`#post_${id}`);

    //Remove Edit function checks to see if an editfield exists and removes it.
    remove_edit(true, id);
    //Sets edit dropdown menu datasetvalue to 0. This is required in order for dropdown function to work properly in "closing" the element
    let edit_dropdown = document.getElementById(id);

    if (edit_dropdown) { edit_dropdown.dataset.value = '0'; }

    //Global variable that holds the value of the current Post ID and Post Textfield being edited
    current_edit = { 'id': `#post_${id}`, 'innerhtml': post.innerHTML };

    string = post.querySelector('.post_string');
    let edit_field = document.createElement('textarea');
    edit_field.rows = 1;
    button_group = document.createElement('div');
    button_group.className = 'button-group';
    submit_button = document.createElement('button');
    submit_button.textContent = 'Submit';
    submit_button.className = 'edit-submit';
    submit_button.setAttribute('onclick', childcomment ? `PostComment(true)` : `PostComment()`);
    cancel_button = document.createElement('button');
    cancel_button.textContent = 'Cancel';
    cancel_button.setAttribute('onclick', childcomment ? `remove_edit(true)` : `remove_edit()`);
    cancel_button.className = 'edit-cancel';
    edit_field.className = 'edit_field';
    edit_field.innerHTML = childcomment ? '' : string.innerText;
    edit_field.style.height = (edit_field.innerText.scrollHeight) + 'px';
    edit_field.setAttribute("oninput", "onInputHandler.call(this)");

    button_group.append(cancel_button, submit_button);
    if (childcomment == false) {
        post.innerHTML = edit_field.outerHTML;
    }
    else {

        const childcommentdiv = document.createElement('div');
        childcommentdiv.className = 'child-comment';
        childcommentdiv.append(edit_field, button_group);
        const lastElement = post.lastElementChild;
        post.insertBefore(childcommentdiv, lastElement);
        ChangeTextAreaHeight();
        return;
    }
    post.append(button_group);
    ChangeTextAreaHeight();
}
//Cha
function ChangeTextAreaHeight() {
    let edit = document.querySelector('.edit_field');
    edit.style.height = edit.scrollHeight + 'px';
}
function edit_post(id, childcomment = false) {
    if (current_edit === '' || childcomment === true) {
        create_edit_field(id);
    }
    else {
        remove_edit();
        create_edit_field(id);

    }
}

function following() {
    fetch(`/following`)
        .then(response => response.json())
        .then(posts => {
            load_newpage(posts, newset = false);
            add_pagination(posts, undefined, true, followinguser = true);
        })
}

function LoadChildComments(parentID, ChildCommentPage = 1) {
    let parentcomment = document.querySelector(`#post_${parentID}`);

    if (parentcomment.querySelector('.replies-div').dataset.value == "0") {
        parentcomment.querySelector('.replies-div').dataset.value = "1";
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
                if (childcommentDiv) { childcommentDiv.innerHTML = ''; }
                posts.ChildCommentData.forEach((element) => {


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
                if (returndata.NextPage > 0) {
                    let ShowMoreReplies = document.createElement('div');
                    ShowMoreReplies.innerText = 'Show More Replies';
                    ShowMoreReplies.className = 'more-replies';
                    ShowMoreReplies.setAttribute('onclick', `LoadChildComments(${parentID}, ${returndata.NextPage}`);
                    childcommentDiv.append(ShowMoreReplies);
                }
            })

    }
    else {

        parentcomment.querySelector('.child-comment-container').innerHTML = '';
        parentcomment.querySelector('.replies-div').dataset.value = "0";

    }

}
