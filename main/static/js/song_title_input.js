const { createApp } = Vue

function debounce(fn, wait) {
    let timer;
    return function(...args) {
        if (timer) {
            clearTimeout(timer); // clear any pre-existing timer
        }

        const context = this; // get the current context

        timer = setTimeout(() => {
            fn.apply(context, args); // call the function if time expires
        }, wait);
   }
}

createApp({
    created() {
        this.onChange = debounce(event => {
            $.get("/api/music/song/search?title=21%20guns", songs => {
                const result = []
                for (item of songs.tracks.items){
                    result.push(item.name)
                }

                this.songs = result
            })
            console.log(event.target.value)
        }, 250);
      },
    data() {
        return {
            songs: []
        }
    },
    methods: {
        // onChange(event) {
        //     debounce(event => {
        //         console.log('changed value:', event.target.value);
        //         // call fetch API to get results
        //       }, 1000);
        // }
    }
}).mount('#song_title_input')
