Email.send({
    SecureToken : "C973D7AD-F097-4B95-91F4-40ABC5567812",
    To : 'them@website.com',
    From : "you@isp.com",
    Subject : "This is the subject",
    Body : "And this is the body",
	Attachments : [
	{
		name : "smtpjs.png",
		path : "https://networkprogramming.files.wordpress.com/2017/11/smtpjs.png"
	}]
}).then(
  message => alert(message)
);