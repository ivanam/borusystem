function delCookies(){
	
	if (document.cookie && document.cookie != '') {
		
				var cookies = document.cookie.split(';');
				
				for (var i = 0; i < cookies.length; i++) {
					
					if( cookies[i].indexOf('user')!= -1 ){
						
							var cookie = jQuery.trim(cookies[i]);
							
							var name=cookie.split('=');
							
							var nombreUser=name[0];
							
						    document.cookie = nombreUser+ '=' + ';expires=Thu, 01-Jan-1970 00:00:01 GMT;path=/boru';	
					}
				}
	 }
}