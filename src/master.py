import urllib.parse

from buildbot.plugins import changes  # type: ignore
from buildbot.plugins import schedulers, util, worker

from .token import TokenClient


class MasterClient(TokenClient):
    def __init__(self, token, host="127.0.0.1", port=8010, *args, **kwargs):
        super().__init__(token, *args, **kwargs)
        self.host = host
        self.port = port

    @property
    def buildbot_url(self):
        return f"https://{self.host}:{self.port}"

    @property
    def worker_names(self):
        return self.list("workers")

    @property
    def workers(self):
        return [
            worker.Worker(worker_name, client.get(f"/workers/{worker_name}"))
            for worker_name in client.worker_names
        ]

    @property
    def postgres_password(self):
        return self.read("postgres")

    @property
    def www(self):
        return {
            "port": self.port,
            "plugins": {"waterfall_view": {}, "console_view": {}, "grid_view": {}},
        }

    @staticmethod
    def pb(port=9989):
        return {
            "protocols": {"pb": {"port": port}},
        }

    @staticmethod
    def git_poller(repo, rate):
        return changes.GitPoller(
            repo,
            branches=True,
            workdir="gitpoller",
            pollInterval=rate,
        )

    def postgres_url(self, host, db_name="postgres", user="postgres"):
        urllib.parse.quote_plus(self.postgres_password)
        return {f"db_url": "postgresql+psycopg2://{user}:{password}@{host}/{db_name}"}

    def checkout_build(self, name, repo, steps):
        f = util.BuildFactory()
        f.addStep(steps.Git(repourl="repo", mode="incremental"))

        for step in steps:
            f.addStep(steps.ShellCommand(command=step))

        return util.BuilderConfig(name=name, workernames=self.worker_names, factory=f)

    @staticmethod
    def change_source(repo):
        return changes.GitPoller(repourl=repo, branches=True)

    @staticmethod
    def scheduler(name, repo, builders, timeout=300):
        return schedulers.SingleBranchScheduler(
            name=name, treeStableTimer=timeout, builderNames=builders
        )
