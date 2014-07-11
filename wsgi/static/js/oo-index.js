$(function() {
	$('#github-username').keyup(function () {
		var username = this.value;
		if (username.length < 2) {
			return;
		}
		console.log('-->', username);

		$.get(
			'https://api.github.com/users/' + username + '/repos',
			{ type: 'owner' },
			function (data) {
				console.log(data);
				$('#github-repository').autocomplete({
					minLength: 0,
					source: data.map(function (repo) { return repo.name })
				});
			}
		);
	}).focus();
});
