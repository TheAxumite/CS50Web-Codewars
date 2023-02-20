document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', function () { load_mailbox('inbox') });
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', submit_mail);
  document.querySelector('.reply-button').addEventListener('click', reply_mail);



  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('.email-container').style.display = 'none';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {


  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('.email-container').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Archive function that runs when archive button is clicked


  //Retrieve Email based
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      emails.forEach(email => {
        //dictionary that holds a value  of reciepent and sender
        let key = { 'inbox': `From: ${email.recipients}`, 'sent': `To: ${email.sender}`, 'archive': `From: ${email.sender}` };
        let line = document.createElement('div');
        //if email is new the font for the email box becomes bold
        if (email.read == false) { line.className = 'new-email-box'; } else { line.className = 'email-box'; }
        let dots = document.createElement("span");
        dots.className = 'mail-list';
        dots.innerHTML = "⋮⋮";
        line.appendChild(dots);
        let button = '';
        //if view is inbox or archive, an archive or unarchive button is created and added at the end of the line
        if (mailbox === 'inbox') {
          button = `<button class="archive_button" onclick="archiveEmail(${email.id}, true)">Archive</button>`;
        } else if (mailbox === 'archive') {
          button = `<button class="archive_button" onclick="archiveEmail(${email.id}, false)">Unarchive</button>`;
        }
        line.innerHTML += `<a href="#" onclick="open_email(${email.id})">${key[mailbox]} Subject: ${email.subject}</a><span class="date"> Date: ${email.timestamp}</span>${button}`;
        document.querySelector("#emails-view").innerHTML += line.outerHTML;
        
      });


    });

}

async function archiveEmail(id,change) {
 //archives or unarchives email based on what the boolean value of change is
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: change
    })
  })
  //waits 2 seconds before continuing 
  await new Promise(resolve => setTimeout(resolve, 200));
  //loads the appropriate view based on what the boolean value of change is
  load_mailbox(change ? 'inbox' : 'archive');

}

function open_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      console.log(email.read);
      //Hides the email composition fields and inbox view. Displays the email container fields
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('.email-container').style.display = 'block';
      // Clear out composition fields
      document.querySelector('.email-container').style.display.innerHTML = '';
      // Print email
      document.querySelector(".email-header h3").innerHTML = `From: ${email.sender}`;
      document.querySelector(".email-body h2").innerHTML = `Subject: ${email.subject}`;
      document.querySelector(".email-header p").innerHTML = email.timestamp;
      document.querySelector(".email-footer p").innerHTML = email.body;


    });

  // Mark email as read  
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function submit_mail() {

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value,
    })
  })
  load_mailbox('sent')
}


function reply_mail() {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('.email-container').style.display = 'none';


  document.querySelector('#compose-recipients').innerHTML = document.querySelector(".email-header h3").innerHTML;
  document.querySelector('#compose-body').innerHTML = `On ${document.querySelector(".email-header p").innerHTML} <${document.querySelector(".email-header h3").innerHTML.slice(6)}> wrote: ${document.querySelector(".email-footer p").innerHTML} `;
  document.querySelector('#compose-subject').value = `RE: ${document.querySelector(".email-body h2").innerHTML.slice(8)}`;


}



