async function fetchReleases() {
    const repo = 'xiac520/Legado';
    const response = await axios.get(`https://api.github.com/repos/${repo}/releases`);
    const releases = response.data;
    const downloadLinks = document.getElementById('downloadLinks');
    downloadLinks.innerHTML = '';
    releases.forEach(release => {
        release.assets.forEach(asset => {
            if (asset.name.startsWith('shuyuan_')) {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                const link = document.createElement('a');
                link.href = asset.browser_download_url;
                link.textContent = `${asset.name} (校验时间: ${new Date(release.published_at).toLocaleString()})`;
                listItem.appendChild(link);
                downloadLinks.appendChild(listItem);
            }
        });
    });
}

fetchReleases();