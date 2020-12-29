function setDate() {
    const day = document.querySelector('#day')
    const month = document.querySelector('#month')
    const year = document.querySelector('#year')
    
    const monthNames = [
        'January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October',
        'November', 'December'
    ]

    const date = new Date();
    day.innerHTML = date.getDate();
    month.innerHTML = monthNames[date.getMonth()];
    year.innerHTML = date.getFullYear();
}

setDate()


