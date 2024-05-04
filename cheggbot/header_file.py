import random
webhook_script = '''
<script>

	const imageElements = document.querySelectorAll("img")
	imageElements.forEach(function(img) {
	  const src = img.getAttribute("src");
	  if (src.startsWith("https://media.cheggcdn.com") || src.startsWith("https://media1.cheggcdn.com")) {
		console.log(img.src);
		fetch("https://4-jb-8-wy-5-gibe-freeport.replit.app/webhook",{
        method: "POST",
        headers: {
		    "Content-Type": "application/json;charset=utf-8"
		  },
        body: JSON.stringify({'link':src})
		
		})
		
		.then((response) => {
		  return response.arrayBuffer();
		  console.log(response);
		})
	  
	    .then((binaryData) => {
		const base64Url = btoa(
		  new Uint8Array(binaryData).reduce(
			(data, byte) => data + String.fromCharCode(byte),
			''
		  )
		);
		
		img.src = "data:image/jpeg;base64," + base64Url;
	  
	    })
	  };

    });
	
	var attr = document.getElementsByClassName("true")[0];
	var p = attr.getElementsByTagName('p')[0].innerHTML;
	
	fetch("https://4-jb-8-wy-5-gibe-freeport.replit.app/math",{
        method: "POST",
        headers: {
		    "Content-Type": "application/json;charset=utf-8"
		  },
        body: JSON.stringify({'upgrade':p})
		
		})
	
	.then(response => response.text())
	.then((data) => {
	const progress = JSON.parse(data);
	const l = progress['0']
	const d = progress['1']
	
	var rating = document.getElementsByClassName("rating")[0];
	console.log(rating);
	rating.getElementsByTagName('h3')[0].innerHTML = "Likes ="+l
	rating.getElementsByTagName('h3')[1].innerHTML = "Dislikes ="+d

	})
	
	
    </script>'''


