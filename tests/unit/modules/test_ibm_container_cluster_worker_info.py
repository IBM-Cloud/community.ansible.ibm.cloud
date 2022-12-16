# (C) Copyright IBM Corp. 2022.
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


import os

from ansible_collections.community.internal_test_tools.tests.unit.compat.mock import patch
from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import ModuleTestCase, AnsibleFailJson, AnsibleExitJson, set_module_args

from .common import DetailedResponseMock
from plugins.modules import ibm_container_cluster_worker_info


class TestClusterWorkerModuleInfo(ModuleTestCase):
    """
    Test class for ClusterWorker module testing.
    """

    def test_ibm_container_cluster_worker_info_success(self):
        """Test the "list" path - successful."""
        patcher = patch(
            'plugins.modules.ibm_container_cluster_worker_info.Worker.basic_worker_info')
        mock = patcher.start()
        mock.return_value = DetailedResponseMock([])

        set_module_args({
            'name': 'testString',
            'worker_id': "hjszfv"
        })

        with self.assertRaises(AnsibleExitJson) as result:
            os.environ['IC_API_KEY'] = 'noAuthAPIKey'
            ibm_container_cluster_worker_info.main()

        assert result['changed'] is True

        mock.assert_called_once()

        patcher.stop()

    def test_ibm_container_cluster_worker_info_failed(self):
        """Test the "list" path - failed."""
        patcher = patch(
            'plugins.modules.ibm_container_cluster_worker_info.Worker.basic_worker_info')
        mock = patcher.start()
        mock.side_effect = Exception('Error listing worker info')

        set_module_args({
            'name': 'testString',
            'worker_id': "hjszfv"
        })

        with self.assertRaises(AnsibleFailJson) as result:
            os.environ['IC_API_KEY'] = 'noAuthAPIKey'
            ibm_container_cluster_worker_info.main()

        assert result.exception == 'Error listing worker info'

        mock.assert_called_once()

        patcher.stop()
