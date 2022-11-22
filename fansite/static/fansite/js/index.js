'use strict';

(function() {
    // Video Player Resize

    const videoPlayerElement = document.getElementById('video-player-container');
    const headerElement = document.querySelector('header');
    if (videoPlayerElement && headerElement) {
        //const videoIframe = videoPlayerElement.querySelector('iframe');
        window.addEventListener('resize', () => {
            console.log(`Dist: ${document.documentElement.clientHeight - videoPlayerElement.getBoundingClientRect().bottom}`);
            console.log(`Max Height: ${document.documentElement.clientHeight - headerElement.offsetHeight}px`);
            if ((document.documentElement.clientHeight - videoPlayerElement.getBoundingClientRect().bottom) > 0) {
                //videoPlayerElement.style.height = `${videoPlayerElement.getBoundingClientRect().height}px`;
                videoPlayerElement.style.maxHeight = `${document.documentElement.clientHeight - headerElement.offsetHeight}px`;
            }
        }, false);
    }

    // Side Nav

    const sideNavElement = document.getElementById('sidenav');
    //const sideNavContentContainer = document.getElementById('sidenav-content-container');
    const sideNavContent = document.getElementById('sidenav-content');

    function handleSideNavExpandClick(e) {
        e.preventDefault();
        //sideNavElement.classList.toggle('open');

        if (sideNavElement.offsetWidth > 0) {
            sideNavElement.style.width = 0;
        } else {
            sideNavElement.style.width = `${sideNavContent.offsetWidth}px`;
        }
    }
    const sideNavExpandBtns = document.querySelectorAll('.sidenav-expand-btn');
    if (sideNavExpandBtns) {
        sideNavExpandBtns.forEach(sideNavExpandBtn => {
            sideNavExpandBtn.addEventListener('click', handleSideNavExpandClick, false);
        });
    }

    // Gallery Slider

    class ImageSlider {
        constructor(element, startIndex = 0) {
            this._element = element;
            this._selectedIndex = startIndex;
            this._imgCount = element.querySelectorAll('.gallery-slider-item').length;
        }

        get element() {
            return this._element;
        }

        get selectedIndex() {
            return this._selectedIndex;
        }
    
        set selectedIndex(newIndex) {
            if (newIndex < 0) {
                this._selectedIndex = this._imgCount - 1;
            } else if (newIndex >= this._imgCount) {
                this._selectedIndex = 0;
            } else {
                this._selectedIndex = newIndex;
            }
        }

        handleGalleryItemSelect(newSelectedIndex) {
            if (newSelectedIndex === this.selectedIndex) return;
    
            // Get direction of slide
            const direction = (newSelectedIndex < this.selectedIndex) ? 'right' : 'left';
    
            // Alter current selected gallery item
            const currSelectedGalleryItem = this.element.querySelector(`.gallery-slider-item[data-index="${this.selectedIndex}"]`);
            currSelectedGalleryItem.style.animationName = `slide-${direction}-from-in`;
            currSelectedGalleryItem.classList.remove('selected-slider-item');
    
            // Alter current selected gallery counter item
            const currSelectedGalleryCounterItem = this.element.querySelector(`.gallery-counter-item[data-index="${this.selectedIndex}"]`);
            currSelectedGalleryCounterItem.classList.remove('selected-slider-counter-item');
    
            this.selectedIndex = newSelectedIndex;
    
            // Alter new selected gallery item
            const newSelectedGalleryItem = this.element.querySelector(`.gallery-slider-item[data-index="${this.selectedIndex}"]`);
            newSelectedGalleryItem.style.animationName = `slide-${direction}-from-out`;
            newSelectedGalleryItem.classList.add('selected-slider-item');
    
            // Alter new selected gallery counter item
            const newSelectedGalleryCounterItem = this.element.querySelector(`.gallery-counter-item[data-index="${this.selectedIndex}"]`);
            newSelectedGalleryCounterItem.classList.add('selected-slider-counter-item');
        }
    
        handlePrevClick() {
            this.handleGalleryItemSelect(this.selectedIndex - 1);
        }
    
        handleNextClick() {
            this.handleGalleryItemSelect(this.selectedIndex + 1);
        }

        init() {
            // Return if only one gallery item
            if (this._imgCount > 1) {

                // Prev Button
                const prevBtn = this.element.querySelector('.gallery-slider-prev');
                if (prevBtn) {
                    prevBtn.addEventListener('click', this.handlePrevClick.bind(this), false);
                }

                // Next Button
                const nextBtn = this.element.querySelector('.gallery-slider-next');
                if (nextBtn) {
                    nextBtn.addEventListener('click', this.handleNextClick.bind(this), false);
                }
            }

            // Add event listeners to slider count items
            const sliderCountItemNodeList = this.element.querySelectorAll('.gallery-counter-item');
            if (sliderCountItemNodeList.length) {
                sliderCountItemNodeList.forEach((sliderCountItem) => {
                    sliderCountItem.addEventListener('click', () => {
                        this.handleGalleryItemSelect(+sliderCountItem.dataset.index);
                    }, false);
                });
            }

            // Add selected classes base on selected index
            const selectedSliderItem = this.element.querySelector(`.gallery-slider-item[data-index="${this.selectedIndex}"]`);
            if (selectedSliderItem) {
                selectedSliderItem.classList.add('selected-slider-item');
            }
            const selectedCounterItem = this.element.querySelector(`.gallery-counter-item[data-index="${this.selectedIndex}"]`);
            if (selectedCounterItem) {
                selectedCounterItem.classList.add('selected-slider-counter-item');
            }
        }
    }

    // Add all image sliders
    const imageSlidersNodeList = document.querySelectorAll('.gallery-slider');
    if (imageSlidersNodeList.length) {
        imageSlidersNodeList.forEach((imgSliderElement) => {
            new ImageSlider(imgSliderElement).init();
        });
    }

    // URL Search Param On Change Handlers
    function urlSearchParamOnChange(e) {
        const searchParams = new URLSearchParams(location.search);

        if (searchParams.has(e.target.name) && searchParams.get(e.target.name) !== e.target.value) {
            searchParams.set(e.target.name, e.target.value);
            location.href = location.origin + location.pathname + '?' + searchParams.toString();
        }
    }

    let selectElement;
    ['sort-type-select', 'sort-direction-select', 'max-displayed-select']
        .forEach((elementID) => {
            selectElement = document.getElementById(elementID);
            if (selectElement) {
                selectElement.addEventListener('change', urlSearchParamOnChange);
            }
        });
})();
