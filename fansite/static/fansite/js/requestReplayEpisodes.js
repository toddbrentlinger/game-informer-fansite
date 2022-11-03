'use strict';

(function() {
    const btn = document.getElementById('get-replay-episodes-btn');
    const randReplayEpisodeElement = document.getElementById('rand-replay-episode');
    const url = '/replay/get/ajax/random-replay-episode';

    if (btn && randReplayEpisodeElement) {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            fetch(url)
                .then((response) => response.text())
                .then((data) => {
                    randReplayEpisodeElement.innerHTML = data;
                });
        });
    }
})();