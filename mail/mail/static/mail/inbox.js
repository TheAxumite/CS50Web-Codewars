document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', function () { load_mailbox('inbox') });
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', submit_mail);


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Retrieve Email based
  

  
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      emails.forEach(email =>{
      let key = {'inbox': `From: ${email.recipients}`, 'sent': `To: ${email.sender}`}
      let line = document.createElement('div');
      let checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      line.className = 'email-box';
      let dots = document.createElement("span");
      dots.innerHTML = "⋮⋮";
      line.appendChild(dots);
      line.appendChild(checkbox);
      line.innerHTML += `<a href="#" ${onclick=open_email(email.id)} ${key[mailbox]} Subject: ${email.subject}, Date: ${email.timestamp}</a>`;
      document.querySelector("#emails-view").innerHTML+= line.outerHTML;
      
      
    });
    
    
  });
}

function open_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Print email
      
      // ... do something else with email ...
    });
}

function submit_mail() {
  console.log(document.querySelector('#compose-recipients').value);
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  load_mailbox('sent')
}
