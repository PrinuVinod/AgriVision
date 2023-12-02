const scriptURL = 'https://script.google.com/macros/s/AKfycby16_-vfX_xHjFyyIlfIlUf1IQa7G003SZFOjE4506yWPeo4EcIBa_DVxZBBXPr59XUMQ/exec'
			const form = document.forms['contactForm']
		  
			form.addEventListener('submit', e => {
			  e.preventDefault()
			  fetch(scriptURL, { method: 'POST', body: new FormData(form)})
				.then(response => alert("Thank you! We will contact you soon." ))
				.catch(error => console.error('Error!', error.message))
			})