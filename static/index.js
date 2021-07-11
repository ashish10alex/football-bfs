
const fruits = ['apple', 'orange', 'banana', 'pear', 'messi', 'ronaldo', 'neymar', 'ramos']

const fuse = new Fuse(fruits)


name_element = document.getElementById('name')
name_element.addEventListener('input', (e) => {
    console.log(e.target.value)
    out = fuse.search(e.target.value)
    console.log(out)
})
