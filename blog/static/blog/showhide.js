function showhide(butID, divID) {
    var item = document.getElementById(divID);
    var but = document.getElementById(butID);
        if (item.className =='hidden') {
            item.className = 'unhidden';
            but.textContent = 'hide';
        }
        else{
            item.className  = 'hidden';
            but.textContent = 'show';
        }
}
