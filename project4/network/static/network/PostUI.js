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