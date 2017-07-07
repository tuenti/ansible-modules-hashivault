import os
import unittest
import sys

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor

def run_playbook(name):
    variable_manager = VariableManager()
    loader = DataLoader()
    inventory = Inventory(loader=loader, variable_manager=variable_manager)

    module_path = ":".join([
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "ansible", "modules", "hashivault"),
    ])

    # Taken from https://stackoverflow.com/a/38067407/28855
    Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='local', module_path=module_path, forks=10, remote_user=None, private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False, become_method=None, become_user=None, verbosity=None, check=False)

    path = os.path.join(os.path.dirname(__file__), name)

    executor = PlaybookExecutor(playbooks=[path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=None)
    return executor.run()

class TestAudit(unittest.TestCase):
    def test_audit(self):
        assert 0 == run_playbook("test_audit.yml"), "exit status != 0"

if __name__ == '__main__':
    unittest.main()
