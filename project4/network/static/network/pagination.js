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
        console.log(page_number)

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

