// ==UserScript==
// @name         Pixiv Image Proxy
// @version      1.0
// @match        *://www.pixiv.net/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function replacePximgLinks() {
        const links = document.querySelectorAll('a[href*="i.pximg.net"]');
        const images = document.querySelectorAll('img[src*="i.pximg.net"]');

        links.forEach(link => {
            link.href = link.href.replace('https://i.pximg.net', 'http://127.0.0.1:5181');
        });

        images.forEach(image => {
            image.src = image.src.replace('https://i.pximg.net', 'http://127.0.0.1:5181');
        });
    }

    replacePximgLinks();

    // Listen for changes in the DOM, in case the page uses AJAX to load content
    const observer = new MutationObserver(replacePximgLinks);
    observer.observe(document.body, { subtree: true, childList: true });
})();
