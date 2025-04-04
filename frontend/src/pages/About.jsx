import 'bootstrap/dist/css/bootstrap.min.css';
import { useEffect, useState } from 'react';

function About() {
    const teamMembers = [
        {
            name: "Milan Dhaduk",
            commitUsername: "mdhaduk",
            issueUsername: "mdhaduk",
            bio: "Sophomore year Computer Science at The University of Texas at Austin",
            responsibilities: "Full stack, Instance development",
            img: "https://miro.medium.com/v2/resize:fit:580/format:webp/1*oJeEFuioGXTVa_VSI6vadw.png",
            tests: 15
        },
        {
            name: "Audrey Tan",
            commitUsername: "akt2468",
            issueUsername: "akt2468",
            bio: "Junior Computer Science major at University of Texas at Austin.",
            responsibilities: "Full stack, Documentation",
            img: "https://miro.medium.com/v2/resize:fit:640/format:webp/1*8A7XXconEuan7zIsmVSLqQ.jpeg",
            tests: 11
        },
        {
            name: "Pooja Vasanthan",
            commitUsername: "PoojaVasanthan",
            issueUsername: "PoojaVasanthan10",
            bio: "Junior year Computer Science major and Statistics and Data Science Minor at UT Austin",
            responsibilities: "Full stack, Instance Development, Documentation",
            img: "https://miro.medium.com/v2/resize:fit:640/format:webp/1*-GfS-B3ALo1LZKA4ZGgW0w.png",
            tests: 19
        },
        {
            name: "Zakaria Sisalem",
            commitUsername: "zak S",
            issueUsername: "sisalemz",
            bio: "3rd year CS & Math major at UT Austin",
            responsibilities: "Full stack, Technical Writing",
            img: "https://miro.medium.com/v2/resize:fit:720/format:webp/1*uQsOHbb6Kn6j_s27hpC-Bg.jpeg",
            tests: 17
        }
    ];

    const [memberStats, setMemberStats] = useState({});

    useEffect(() => {
        let authorCommits = {};
        let authorIssues = {};
        let seenCommits = new Set(); // To store unique commit SHAs

        teamMembers.forEach(member => {
            authorCommits[member.name] = 0;
            authorIssues[member.name] = 0;
        });

        const projectId = "66936503";

        // Step 1: Fetch all branches
        fetch(`https://gitlab.com/api/v4/projects/${projectId}/repository/branches`)
            .then(response => response.json())
            .then(branches => {
                const commitPromises = branches.map(branch =>
                    fetch(`https://gitlab.com/api/v4/projects/${projectId}/repository/commits?ref_name=${branch.name}&per_page=100`)
                        .then(response => response.json())
                        .then(commits => {
                            commits.forEach(commit => {
                                // Avoid counting duplicate commits across branches
                                if (!seenCommits.has(commit.id)) {
                                    seenCommits.add(commit.id);
                                    let mappedName = teamMembers.find(member => member.commitUsername === commit.author_name)?.name;
                                    if (mappedName) {
                                        authorCommits[mappedName] = (authorCommits[mappedName] || 0) + 1;
                                    }
                                }
                            });
                        })
                );

                return Promise.all(commitPromises);
            })
            .then(() => {
                // Step 2: Fetch issues for each member
                const issuePromises = teamMembers.map(member =>
                    fetch(`https://gitlab.com/api/v4/projects/${projectId}/issues?author_username=${member.issueUsername}&per_page=100`)
                        .then(response => response.json())
                        .then(issues => {
                            authorIssues[member.name] = issues.length;
                        })
                        .catch(error => console.error(error))
                );

                return Promise.all(issuePromises);
            })
            .then(() => {
                // Step 3: Update state with fetched data
                const updatedMemberStats = {};
                teamMembers.forEach(member => {
                    updatedMemberStats[member.name] = {
                        commits: authorCommits[member.name] || 0,
                        issues: authorIssues[member.name] || 0,
                        unitTests: 0,
                    };
                });

                setMemberStats(updatedMemberStats);
            })
            .catch(error => console.error(error));
    }, []);

    return (
        <div className="container mt-5">
            <h1 className="text-center">About WildWareness</h1>
            <p className="text-center">
                WildWareness is a web application designed to provide help and spread awareness 
                about fires in California by providing real-time information on wildfire incidents, 
                emergency shelters, and community-reported fire updates.
            </p>
            <hr />

            <div className="row justify-content-center">
                <div className="col-12">
                    <h2 className="text-center">Team Members</h2>
                </div>

                {teamMembers.map((member, index) => (
                    <div key={index} className="col-md-4 text-center" id='member-card'>
                        <img src={member.img} className="rounded-circle member-photo" style={{ padding: "5px" }} alt={member.name} width="150" />
                        <h4>{member.name}</h4>
                        <p><strong>Bio:</strong> {member.bio}</p>
                        <p><strong>Major Responsibilities:</strong> {member.responsibilities}</p>
                        <p className="member-stats"><strong>Stats:</strong><br />
                            Commits: {memberStats[member.name]?.commits || 0}<br />
                            Issues: {memberStats[member.name]?.issues || 0}<br />
                            Unit Tests: {member.tests}
                        </p>
                    </div>
                ))}
            </div>

            <div className="container mt-5">
                <div className="row">
                    <div className="col-6">
                        <p className="text-center"><strong>Data Sources</strong></p>
                        <ul>
                            <li><a href="https://www.fire.ca.gov/incidents/2025" target="_blank">CAL FIRE</a> - Reports active and past wildfires.</li>
                            <li><a href="https://www.thenewsapi.com/documentation" target="_blank">TheNewsAPI</a> - Fetches local reports and headlines.</li>
                            <li><a href="https://mapsplatform.google.com/pricing/?utm_source=google&utm_medium=cpc&utm_campaign=gmp25_us_search_api&gad_source=1&gclid=CjwKCAjwp8--BhBREiwAj7og1_8QWnO-NMYt295SA5xAZgVTAEWjR5t_f_M6DDBTlr6awfqMmf4eRRoC5IAQAvD_BwE&gclsrc=aw.ds" target="_blank">Google Maps API</a> - Fetches location info.</li>
                            <li><a href="https://leafletjs.com/" target="_blank">Leaflet</a> - Gets map rendering.</li>
                            <li><a href="https://console.cloud.google.com/marketplace/product/google/geocoding-backend.googleapis.com?q=search&referrer=search&project=hardy-position-450923-v1" target="_blank">Google Maps Geocoding API</a> - Converts coordinates.</li>
                            <li><a href="https://developers.google.com/custom-search/v1/overview" target="_blank">Google Custom Search API</a> - Search using Google's Custom Search.</li>
                        </ul>
                    </div>
                    <div className="col-6">
                        <p className="text-center"><strong>Tools</strong></p>
                        <ul>
                            <li>Bootstrap Framework</li>
                            <li>React</li>
                            <li>Python</li>
                            <li>Docker</li>
                            <li>Google Maps</li>
                            <li>Amazon Route 53</li>
                            <li>Selenium, Postman, Jest, and UnitTest Frameworks</li>
                            <li>AWS Hosting</li>
                            <li>Visual Studio Code</li>
                            <li>GitLab</li>
                        </ul>
                    </div>
                    <div className="col-12 mt-3" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <p className="text-center"><strong>GitLab Repo Link</strong></p>
                        <a href="https://gitlab.com/mdhaduk1/cs373-spring-2025-group-03/-/tree/development?ref_type=heads">Click Here</a>
                    </div>
                    <div className="col-12 mt-3" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <p className="text-center"><strong>API Postman Documentation</strong></p>
                        <a href="https://documenter.getpostman.com/view/31322139/2sAYdZvEUy">Click Here</a>
                    </div>
                    <div className="col-12 mt-3" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <p className="text-center"><strong>API (Test) Endpoints</strong></p>
                        <a href="https://api.wildwareness.net/shelters">https://api.wildwareness.net/shelters</a>
                        <a href="https://api.wildwareness.net/shelters/1">https://api.wildwareness.net/shelters/1</a>
                    </div>
                    <div className="col-12 mt-3">
                        <p className="text-center"><strong>Significance of Data</strong></p>
                        <p>
                        By overlaying wildfire incident data with emergency shelter locations, we can 
                        identify coverage gaps where communities may not have nearby safe zones. Real-time 
                        tracking of wildfire spread can predict when shelters will become overwhelmed, allowing 
                        authorities to proactively open new locations. Crowdsourced community reports can act 
                        as an early detection mechanism, sometimes catching fires before they are officially reported. 
                        Cross-referencing these reports with satellite and weather data can improve fire
                        risk prediction models. The fusion of wildfire data, emergency response infrastructure, 
                        and real-time community input creates a smarter, more adaptive disaster 
                        management system. It enables faster responses, better resource allocation, and 
                        data-driven policy decisions to mitigate wildfire damage and save lives.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default About;
