from typing import Annotated

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field


server = MCPServer(
    name="code-reviewer",
    version="0.1.0",
    instructions=(
        "This learning server returns deterministic mock repository data and never "
        "changes external state. Read the pull request before requesting its changed files."
    ),
)

READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    openWorldHint=False,
)

RepositoryOwner = Annotated[str, Field(min_length=1, description="Repository owner or organization.")]
RepositoryName = Annotated[str, Field(min_length=1, description="Repository name.")]
PullNumber = Annotated[int, Field(gt=0, description="Pull request number.")]
IssueNumber = Annotated[int, Field(gt=0, description="Issue number.")]


class PullRequest(BaseModel):
    id: str
    number: int
    title: str
    state: str
    author: str
    base: str
    head: str
    body: str
    url: str


class PullRequestResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pull_request: PullRequest = Field(alias="pullRequest")


class ChangedFile(BaseModel):
    path: str
    status: str
    additions: int
    deletions: int
    patch: str


class ChangedFilesResult(BaseModel):
    files: list[ChangedFile]


class Issue(BaseModel):
    id: str
    number: int
    title: str
    state: str
    body: str
    labels: list[str]
    url: str


class IssueResult(BaseModel):
    issue: Issue


@server.tool(
    title="Get pull request",
    description="Get the metadata and description for one pull request before reviewing its changes.",
    annotations=READ_ONLY,
    structured_output=True,
)
def get_pull_request(
    owner: RepositoryOwner,
    repository: RepositoryName,
    pullNumber: PullNumber,
) -> PullRequestResult:
    """Return deterministic pull-request data for the MCP learning exercise."""
    return PullRequestResult(
        pull_request=PullRequest(
            id=f"PR_{pullNumber}",
            number=pullNumber,
            title="Harden the authentication callback",
            state="open",
            author="octo-reviewer",
            base="main",
            head="feature/auth-callback",
            body="Updates callback handling and adds an audit endpoint.",
            url=f"https://example.invalid/{owner}/{repository}/pull/{pullNumber}",
        )
    )


@server.tool(
    title="Get changed files",
    description="Get file metadata and unified patches for the files changed by a pull request.",
    annotations=READ_ONLY,
    structured_output=True,
)
def get_changed_files(
    owner: RepositoryOwner,
    repository: RepositoryName,
    pullNumber: PullNumber,
) -> ChangedFilesResult:
    """Return deterministic changed-file data for the MCP learning exercise."""
    del owner, repository, pullNumber

    files = [
        ChangedFile(
            path="src/auth/callback.js",
            status="modified",
            additions=5,
            deletions=2,
            patch="\n".join(
                [
                    "@@ -18,4 +18,7 @@ export async function callback(req, db) {",
                    "-  const user = await db.findUser(req.query.email);",
                    "+  const sql = `SELECT * FROM users WHERE email = '${req.query.email}'`;",
                    "+  const user = await db.query(sql);",
                    "+  await db.query(`INSERT INTO audit(message) VALUES ('login:${req.query.email}')`);",
                    "   return createSession(user);",
                    " }",
                ]
            ),
        ),
        ChangedFile(
            path="src/audit/report.js",
            status="added",
            additions=8,
            deletions=0,
            patch="\n".join(
                [
                    "@@ -0,0 +1,8 @@",
                    "+export async function buildReport(users, db) {",
                    "+  const report = [];",
                    "+  for (const user of users) {",
                    "+    report.push(await db.getAuditEvents(user.id));",
                    "+  }",
                    "+  return report;",
                    "+}",
                ]
            ),
        ),
    ]

    return ChangedFilesResult(files=files)


@server.tool(
    title="Get issue",
    description="Get an issue that may provide requirements or context for a code review.",
    annotations=READ_ONLY,
    structured_output=True,
)
def get_issue(
    owner: RepositoryOwner,
    repository: RepositoryName,
    issueNumber: IssueNumber,
) -> IssueResult:
    """Return deterministic issue data for the MCP learning exercise."""
    return IssueResult(
        issue=Issue(
            id=f"ISSUE_{issueNumber}",
            number=issueNumber,
            title="Record authentication events for compliance reporting",
            state="open",
            body="Log successful callbacks without storing credentials or secrets.",
            labels=["security", "audit"],
            url=f"https://example.invalid/{owner}/{repository}/issues/{issueNumber}",
        )
    )


if __name__ == "__main__":
    server.run(transport="stdio")
