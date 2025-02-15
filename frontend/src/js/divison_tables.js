document.addEventListener('DOMContentLoaded', () => {
    const div1Button = document.getElementById('div1-button');
    const div1Table = document.getElementById('div1-table');
    const div2Button = document.getElementById('div2-button');
    const div2Table = document.getElementById('div2-table');

    function setupTable() {
        const fragment = window.location.hash.substring(1);

        if (fragment == 'div1') {
            showDiv1();
        } else if (fragment == 'div2') {
            showDiv2();
        }
    }

    function showTable(buttonToShow, buttonToHide, tableToShow, tableToHide) {
        buttonToShow.classList.add('is-active');
        buttonToHide.classList.remove('is-active');
        tableToShow.classList.remove('is-hidden');
        tableToHide.classList.add('is-hidden');
    }

    function showDiv1() {
        showTable(div1Button, div2Button, div1Table, div2Table);

        window.location.hash = 'div1';
    }

    function showDiv2() {
        showTable(div2Button, div1Button, div2Table, div1Table);

        window.location.hash = 'div2';
    }

    if (window.location.pathname == '' || window.location.pathname == '/') {
        setupTable();

        div1Button.addEventListener('click', showDiv1);
        div2Button.addEventListener('click', showDiv2);
    }
});
