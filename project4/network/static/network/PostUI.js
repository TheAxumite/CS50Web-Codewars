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
    submit_button.setAttribute('onclick', childcomment ? `PostComment()` : `editComment()`);
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
function showMoreReplies(parentID, nextpage) {
    let ShowMoreReplies = document.createElement('div');
    ShowMoreReplies.innerText = 'Show More Replies';
    ShowMoreReplies.className = 'more-replies';
    ShowMoreReplies.style.cursor = 'pointer';
    ShowMoreReplies.setAttribute('onclick', `LoadChildComments(${parentID}, ${nextpage})`);
    return ShowMoreReplies;
}

//used to remove strings only and retrieve post number from a post element
function removeLetters(str) {
    return str.replace(/[^\d]/g, '');
};


function autoGrow(edit_field) {
    edit_field.style.height = 'auto';
    edit_field.style.height = (edit_field.scrollHeight) + 'px';
}


function onInputHandler() {
    autoGrow(this);
}

//button hover listner  for Follow button

const follow_icon = document.createElement('div');
const followuser = document.createElement('button');
followuser.innerText = 'Follow';
followuser.style.width = '128px';
followuser.style.height = '32px';
followuser.style.cursor = 'pointer';
const csrfToken = document.querySelector('#csrf_token').value;
followuser.setAttribute('data-csrf-token', csrfToken);
//follow button attribute when clicked runs the follow function
followuser.setAttribute('onclick', `follow()`);
follow_icon.append(followuser);


function changeRepliesfunction(postNumber) {
    post = document.querySelector(postNumber);
    replies = post.querySelector('.replies-div');
    reply = replies.querySelector('.reply-text');
    reply.setAttribute('onclick', `removeChildComments('${postNumber}')`)

}

function removeChildComments(postNumber) {
    post = document.querySelector(postNumber);
    childcomment = post.querySelector('.child-comment-container');
    childcomment.innerHTML = '';
    replies = post.querySelector('.replies-div');
    reply = replies.querySelector('.reply-text');
    reply.setAttribute('onclick', `LoadChildComments('${removeLetters(postNumber)}', ${1})`);

}

function createNavItem(text, ul, following = false) {
    const item = document.createElement('li');
    item.className = 'page-item';
    const link = document.createElement('a');
    link.className = 'page-link .bg-dark';
    link.innerText = text;
    link.addEventListener("click", function (event) {
        PageTracker.page_selection(event, following);
    });
    item.appendChild(link);
    ul.appendChild(item);

}