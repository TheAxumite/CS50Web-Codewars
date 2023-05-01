document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#post-button').addEventListener('click', function () { create_post });
    document.querySelector('#profile').addEventListener('click', function () { load_posts_profile('user') })
    document.querySelector('#allposts').addEventListener('click', () => load_posts_profile('allposts'))
    load_posts_profile('allposts')

});

class CreateElements {
    constructor() { }


    createLikeButton(buttonAttribute = {
        className: 'like_button',
        backgroundColor: '#23232452',
        border: 'transparent',
    }) {
        const button = document.createElement('button');
        button.className = buttonAttribute.className;
        button.style.backgroundColor = buttonAttribute.backgroundColor;
        button.style.border = buttonAttribute.border;
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
        path.setAttribute('d', 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z');
        // append path element to SVG element
        svg.appendChild(path);
        button.appendChild(svg)
        return button;
    }

    createFollowIcon(IconAttribute = {
        src: "{% static 'network/follow.png' %}",
        className: 'follow_icon',
        width: '64px',
        height: '64px',
        cursor: 'pointer',
        display: 'inline-block',
    }) {
        const follow_icon = document.createElement('img');
        follow_icon.src = IconAttribute.src;
        follow_icon.className = IconAttribute.className;
        follow_icon.style.width = IconAttribute.width;
        follow_icon.style.height = IconAttribute.height;
        follow_icon.style.cursor = IconAttribute.cursor;
        follow_icon.style.display = IconAttribute.display;
        return follow_icon;
    }

    createNavItem(NavAttribute = { ItemClassName: 'page-item', LinkClassName: 'page-link'}, text, ul, clickHandler) {
        const item = document.createElement('li');
        item.className = NavAttribute.ItemClassName;
        const link = document.createElement('a');
        link.className = NavAttribute.LinkClassName;
        link.innerText = text;
        link.addEventListener("click", clickHandler);
        item.appendChild(link);
        ul.appendChild(item);
        
    }

    CreateRepliesIcon(RepliesAttribute = { RepliesClassName: 'replies-div', ReplyClassName:'reply-text'
        
    })
    {
        const replies = document.createElement('div');
        replies.className = 'replies-div'
        const reply = document.createElement('span');
        reply.className = 'replies-text';
        reply.
    }
}
    

