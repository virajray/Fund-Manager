function addPayment(studentId) {
    const month = document.getElementById(`month-${studentId}`).value;
    const amountPaid = document.getElementById(`amount-${studentId}`).value;

    if (!month || !amountPaid) {
        alert("Please select a month and enter an amount.");
        return;
    }

    // Confirmation dialog
    if (!confirm(`Are you sure you want to add a payment of LKR ${amountPaid} for ${month}?`)) {
        return;
    }

    fetch('/admin/add_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: studentId,
            month: month,
            amount_paid: parseFloat(amountPaid),
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload(); // Reload the page after successful payment
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while adding the payment.');
    });
}