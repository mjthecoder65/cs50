function StopWatch() {
    let running = false, duration = 0;
    let clearIntervalId = 0;

    this.start= () => {
        running = true;
        clearIntervalId = setInterval(()=>{
            duration += 1;
        }, 1000)
    }
    this.stop = () => {
        clearInterval(clearIntervalId)
        let hours = Math.floor(duration / (3600 * 1000));
        duration = duration - (3600 * hours)
        let minutes = Math.floor(duration / (60 * 1000))
        duration = duration - (minutes * 600)
        let seconds = Math.floor(duraton / 1000);
        duration = 0;
        return { hours, minutes, seconds}
    }
    this.restart = () => {
        clearInterval(clearIntervalId)
        duration = 0    
    }
}
const stopwatch = new StopWatch();

const startButton = document.querySelector('#startWorking');
const stopButton = document.querySelector('#stopWorking');
startButton.addEventListener("click", () => {
    // show stop button 
    stopButton.style.display = 'block';
    stopwatch.start();
});

stopButton.addEventListener('click', () => {
    // Hide start button 
    startButton.style.display = 'block';
    let time = stopwatch.stop();
    document.getElementById('hours').innerHTML = `${time.hours}`
    document.getElementById('minutes').innerHTML = `${time.minutes}`
    document.getElementById('seconds').innerHTML = `${time.seconds}`
});


