Pod Failure
=========

Use this role to kill a specific pod by providing cluster id, pod name and namespace it belongs to as an inputs.

Requirements
------------

The below requirements are needed on the host that executes k8s module.

python >= 3.6
kubernetes >= 12.0.0
PyYAML >= 3.11
jsonpatch


Example Playbook
----------------

  - name: Running pre-task
    hosts: localhost

    # User input variables
    vars_prompt:
      - name: pod_name
        prompt: Enter pod name
  
      - name: k8s_namespace
        prompt: Enter k8s namespace

   #Execute before tasks
   pre_tasks:
   - set_fact:
      # Making varaible values accessible across repo
      zip_path: /tmp/kubeConfig-{{ cluster_id }}.zip
      kube_config_path: /tmp/kubeConfig-{{ cluster_id }}
      IC_IAM_TOKEN: "{{ lookup('env','IC_IAM_TOKEN') }}"
      IC_IAM_REFRESH_TOKEN: "{{ lookup('env','IC_IAM_REFRESH_TOKEN') }}"
      pod_name: "{{ pod_name }}"
      k8s_namespace: "{{ k8s_namespace }}"

  - name: Install k8s module
    pip:
      name: k8s
      extra_args: --user
      state: present

    - name: Make kubernetes pod {{ pod_name }} down
      hosts: localhost
        roles:
          - role: ./roles/pod_failure

