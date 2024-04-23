// Function to handle the drag start event
function dragStart(event) {
  event.dataTransfer.setData('text/plain', event.target.id);
}

// Function to handle the drag over event
function allowDrop(event) {
  event.preventDefault();  // Necessary to allow a drop
}

// Function to handle the drop event
function drop(event) {
  event.preventDefault();
  // const ticketId =
  //     event.dataTransfer.getData('text/plain').replace('ticket', '');
  const ticketId = event.dataTransfer.getData('text/plain')
  const ticket = document.getElementById(ticketId);
  const dropzone = event.target.closest('.dropzone');

  if (dropzone) {
    dropzone.appendChild(ticket);
    const newStatus = dropzone.getAttribute('data-status');

    // AJAX call to Flask backend to update the ticket's status
    fetch('/update_ticket_status', {
      method: 'POST',
      body: JSON.stringify({
        ticket_id: ticketId,
        new_status: dropzone.getAttribute('data-status')
      }),
      headers: {
        'Content-Type': 'application/json',
      }
    })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Failed to move ticket');
          }
        })
        .then(data => {
          console.log(data.message);  // Log the success message from the server
        })
        .catch(error => {
          console.error('Error:', error);
        });
  }
}
