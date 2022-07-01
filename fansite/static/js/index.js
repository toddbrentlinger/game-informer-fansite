'use strict';

(function() {
    const videoPlayerElement = document.getElementById('video-player-container');
    if (videoPlayerElement) {
        //const videoIframe = videoPlayerElement.querySelector('iframe');
        window.addEventListener('resize', () => {
            console.log(`Dist: ${document.documentElement.clientHeight - videoPlayerElement.getBoundingClientRect().bottom}`);
            if ((document.documentElement.clientHeight - videoPlayerElement.getBoundingClientRect().bottom) > 0) {
                //videoPlayerElement.style.height = `${videoPlayerElement.getBoundingClientRect().height}px`;
            }
        }, false);
    }

    const sideNavElement = document.getElementById('sidenav');
    function handleSideNavExpandClick(e) {
        e.preventDefault();
        sideNavElement.classList.toggle('open');
    }
    const sideNavExpandBtns = document.querySelectorAll('.sidenav-expand-btn');
    if (sideNavExpandBtns) {
        sideNavExpandBtns.forEach(sideNavExpandBtn => {
            sideNavExpandBtn.addEventListener('click', handleSideNavExpandClick, false);
        });
    }
})();