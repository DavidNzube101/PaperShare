
// Get references to the modal and buttons
const modal = document.getElementById('modal');
try{
    const closeModalBtn = document.getElementById('closeModalBtn');

    // Close the modal
    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
} catch (error) {
    console.log('error')
}


// Close the modal if the user clicks outside the modal content
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});