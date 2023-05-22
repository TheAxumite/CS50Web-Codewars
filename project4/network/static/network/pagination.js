 //Function responsible for creating and managing pagination functionality for posts.
 function add_pagination(postdata, pagedata = null, windowload = false, following = false) {
    //clear variable
    current_edit = '';
    // Get the container for all posts and create a new navigation element.
    const allPosts = document.querySelector(".all_posts");
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Page navigation example');
    const ul = document.createElement('ul');
    ul.className = 'pagination justify-content-center';
    // Add a 'Previous' navigation item to the unordered list if page number is greater than 1
    if (pagedata) {
        if (pagedata.page > 5) {
            createNavItem('Previous', ul, following);
        }
    }
    // Determine the starting page number depending on whether the window has just loaded or not.
    let startPage = windowload ? 1 : postdata.pages_left + 1;
    //Determine if the amount of pages left is less than 5
    let pagesToShow = Math.min(postdata.pages_left, 5);
    // If the window has just loaded, create the pagination items and add them to the unordered list.
    if (windowload) {
        for (let i = startPage; i < startPage + pagesToShow; i++) { item_element(i, ul, following); }
        //Add a Next pagination item if 
        if (parseInt(postdata.pages_left) > 5) { createNavItem('Next', ul, following); }
        nav.appendChild(ul);
        allPosts.appendChild(nav);
    }
    const pageLinks = document.querySelectorAll('.page-link');
    if (!windowload) {
        if (pagedata.next_set === false && pagedata.previous_set === false) {
            counter = PageTracker.LastSet(pagedata, postdata, pageLinks);
            start = PageTracker.FirstSet(pagedata, postdata, pageLinks);
            //Render new set of posts
            load_newpage(postdata, newset = false);
            for (let i = start; i <= counter; i++) {
                item_element(i, ul);
            }
            if (pagedata.page + parseInt(postdata.pages_left) > counter) { createNavItem('Next', ul, following); }
            nav.appendChild(ul);
            allPosts.appendChild(nav);
        } else {
            second_counter = PageTracker.LastSet(pagedata, postdata, pageLinks);
            first_counter = PageTracker.FirstSet(pagedata, postdata, pageLinks);
            load_newpage(postdata, newset = false);
            //Create pagination elements 
            for (let i = first_counter; i <= second_counter; i++) {
                item_element(i, ul);
            }
            if (pagedata.page + parseInt(postdata.pages_left) > second_counter) { createNavItem('Next', ul, following); }
            nav.appendChild(ul);
            allPosts.appendChild(nav);
        }
    }
}