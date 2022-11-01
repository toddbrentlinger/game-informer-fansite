'use strict';

(function() {
    const btn = document.getElementById('get-replay-episodes-btn');

    if (btn) {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            console.log('Get Replay Episodes!');

            const url = '/get/ajax/episodes';

            fetch(url)
                .then(response => {
                    console.log(response);
                });
        });
    }
})();