const members = ["Milan Dhaduk", "Audrey Tan", "Zakaria Sisalem", "Pooja Vasanthan"];
const usernames = ["mdhaduk", "akt2468", "sisalemz", "PoojaVasanthan10"];
const idToName = {"mdhaduk" : "Milan Dhaduk", 
                "akt2468": "Audrey Tan", 
                "sisalemz":"Zakaria Sisalem", 
                "PoojaVasanthan10":"Pooja Vasanthan"}


fetch("https://gitlab.com/api/v4/projects/66936503/repository/commits?per_page=100",
    {
        method: 'GET'
    }
)
.then(response => {
    if (!response.ok) {
      throw new Error('gitlab commit api responded with an error');
    }
    return response.json();
  })
  .then(projectInfo => {
    let authorCommits = {"Milan Dhaduk" : 0, "Audrey Tan" : 0, "Zakaria Sisalem" : 0, "Pooja Vasanthan" : 0}
    for(let i = 0; i < projectInfo.length; i++){
        let author = idToName[projectInfo[i].author_name];
        authorCommits[author]++;
    }
    for(let i = 0; i < 4; i++){
        let stats = document.getElementById(members[i] + " Stats");
        let updated = stats.innerHTML.replace("Commits:", "Commits: " + authorCommits[members[i]]);
        stats.innerHTML = updated;
    }
  })
  .catch(error => console.error(error))

for(let i = 0; i < 4; i++){
  let newFetch = fetch("https://gitlab.com/api/v4/projects/66936503/issues?author_username=" + usernames[i] + "&per_page=100",
    {
      method: 'GET'
    }
  )
  .then(response => {
    if (!response.ok) {
      throw new Error('gitlab issue api responded with an error for ' + usernames[i]);
    }
    return response.json();
  })
  .then(issueInfo => {
    let statsIssues = document.getElementById(members[i] + " Stats");
    let updated = statsIssues.innerHTML.replace("Issues:", "Issues: " + issueInfo.length + " ");
    statsIssues.innerHTML = updated;
  })
  .catch(error => console.error(error));
}

