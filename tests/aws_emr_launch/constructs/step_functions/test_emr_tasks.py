from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import core

from aws_emr_launch.constructs.emr_constructs import emr_code, emr_profile
from aws_emr_launch.constructs.step_functions import emr_tasks


def print_and_assert(default_task_json: dict, task: sfn.Task):
    stack = core.Stack.of(task)
    resolved_task = stack.resolve(task.to_state_json())
    print(default_task_json)
    print(resolved_task)
    assert default_task_json == resolved_task


def test_start_execution_task():
    default_task_json = {
        'End': True,
        'Parameters': {
            'StateMachineArn': {'Ref': 'teststatemachine7F4C511D'},
            'Input.$': '$$.Execution.Input'
        },
        'Type': 'Task',
        'Resource': {
            'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::states:startExecution.sync']]
        }
    }

    stack = core.Stack(core.App(), 'test-stack')

    state_machine = sfn.StateMachine(
        stack, 'test-state-machine',
        definition=sfn.Chain.start(sfn.Succeed(stack, 'Succeeded')))

    task = sfn.Task(
        stack, 'test-task',
        task=emr_tasks.StartExecutionTask(
            state_machine,
        )
    )

    print_and_assert(default_task_json, task)


def test_start_execution_task_with_input():
    default_task_json = {
        'End': True,
        'Parameters': {
            'StateMachineArn': {'Ref': 'teststatemachine7F4C511D'},
            'Input': {'Key1': 'Value1'},
            'Name': 'test-sfn-task'
        },
        'Type': 'Task',
        'Resource': {
            'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::states:startExecution.sync']]
        }
    }

    stack = core.Stack(core.App(), 'test-stack')

    state_machine = sfn.StateMachine(
        stack, 'test-state-machine',
        definition=sfn.Chain.start(sfn.Succeed(stack, 'Succeeded')))

    task = sfn.Task(
        stack, 'test-task',
        task=emr_tasks.StartExecutionTask(
            state_machine,
            input={'Key1': 'Value1'},
            name='test-sfn-task'
        )
    )

    print_and_assert(default_task_json, task)


def test_emr_create_cluster_task():
    default_task_json = {
        'End': True,
        'Parameters': {
            'AdditionalInfo.$': '$.ClusterConfiguration.Cluster.AdditionalInfo',
            'AmiVersion.$': '$.ClusterConfiguration.Cluster.AmiVersion',
            'Applications.$': '$.ClusterConfiguration.Cluster.Applications',
            'AutoScalingRole.$': '$.ClusterConfiguration.Cluster.AutoScalingRole',
            'BootstrapActions.$': '$.ClusterConfiguration.Cluster.BootstrapActions',
            'Configurations.$': '$.ClusterConfiguration.Cluster.Configurations',
            'CustomAmiId.$': '$.ClusterConfiguration.Cluster.CustomAmiId',
            'EbsRootVolumeSize.$': '$.ClusterConfiguration.Cluster.EbsRootVolumeSize',
            'Instances': {
                'AdditionalMasterSecurityGroups.$':
                    '$.ClusterConfiguration.Cluster.Instances.AdditionalMasterSecurityGroups',
                'AdditionalSlaveSecurityGroups.$':
                    '$.ClusterConfiguration.Cluster.Instances.AdditionalSlaveSecurityGroups',
                'Ec2KeyName.$': '$.ClusterConfiguration.Cluster.Instances.Ec2KeyName',
                'Ec2SubnetId.$': '$.ClusterConfiguration.Cluster.Instances.Ec2SubnetId',
                'Ec2SubnetIds.$': '$.ClusterConfiguration.Cluster.Instances.Ec2SubnetIds',
                'EmrManagedMasterSecurityGroup.$':
                    '$.ClusterConfiguration.Cluster.Instances.EmrManagedMasterSecurityGroup',
                'EmrManagedSlaveSecurityGroup.$':
                    '$.ClusterConfiguration.Cluster.Instances.EmrManagedSlaveSecurityGroup',
                'HadoopVersion.$': '$.ClusterConfiguration.Cluster.Instances.HadoopVersion',
                'InstanceCount.$': '$.ClusterConfiguration.Cluster.Instances.InstanceCount',
                'InstanceFleets.$': '$.ClusterConfiguration.Cluster.Instances.InstanceFleets',
                'InstanceGroups.$': '$.ClusterConfiguration.Cluster.Instances.InstanceGroups',
                'KeepJobFlowAliveWhenNoSteps': True,
                'MasterInstanceType.$': '$.ClusterConfiguration.Cluster.Instances.MasterInstanceType',
                'Placement.$': '$.ClusterConfiguration.Cluster.Instances.Placement',
                'ServiceAccessSecurityGroup.$': '$.ClusterConfiguration.Cluster.Instances.ServiceAccessSecurityGroup',
                'SlaveInstanceType.$': '$.ClusterConfiguration.Cluster.Instances.SlaveInstanceType',
                'TerminationProtected.$': '$.ClusterConfiguration.Cluster.Instances.TerminationProtected'
            },
            'JobFlowRole.$': '$.ClusterConfiguration.Cluster.JobFlowRole',
            'KerberosAttributes.$': '$.ClusterConfiguration.Cluster.KerberosAttributes',
            'LogUri.$': '$.ClusterConfiguration.Cluster.LogUri',
            'Name.$': '$.ClusterConfiguration.Cluster.Name',
            'NewSupportedProducts.$': '$.ClusterConfiguration.Cluster.NewSupportedProducts',
            'ReleaseLabel.$': '$.ClusterConfiguration.Cluster.ReleaseLabel',
            'RepoUpgradeOnBoot.$': '$.ClusterConfiguration.Cluster.RepoUpgradeOnBoot',
            'ScaleDownBehavior.$': '$.ClusterConfiguration.Cluster.ScaleDownBehavior',
            'SecurityConfiguration.$': '$.ClusterConfiguration.Cluster.SecurityConfiguration',
            'ServiceRole.$': '$.ClusterConfiguration.Cluster.ServiceRole',
            'StepConcurrencyLevel.$': '$.ClusterConfiguration.Cluster.StepConcurrencyLevel',
            'SupportedProducts.$': '$.ClusterConfiguration.Cluster.SupportedProducts',
            'Tags.$': '$.ClusterConfiguration.Cluster.Tags',
            'VisibleToAllUsers.$': '$.ClusterConfiguration.Cluster.VisibleToAllUsers'
        },
        'Resource':
            {'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::elasticmapreduce:createCluster.sync']]
        },
        'Type': 'Task'
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = sfn.Task(
        stack, 'test-task',
        task=emr_tasks.EmrCreateClusterTask(
            roles=emr_profile.EMRRoles(stack, 'test-emr-roles', role_name_prefix='test-roles'),
            cluster_configuration_path='$.ClusterConfiguration.Cluster',
        )
    )

    print_and_assert(default_task_json, task)


def test_emr_add_step_task():
    default_task_json = {
        'End': True,
        'Parameters': {
            'ClusterId': 'test-cluster-id',
            'Step': {'Key1': {'Key2': 'Value2'}}
        },
        'Resource': {'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::elasticmapreduce:addStep.sync']]},
        'Type': 'Task'
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = sfn.Task(
        stack, 'test-task',
        task=emr_tasks.EmrAddStepTask(
            'test-cluster-id',
            {'Key1': {'Key2': 'Value2'}}
        )
    )

    print_and_assert(default_task_json, task)


def test_load_cluster_configuration_builder():
    default_task_json = {
        'End': True,
        'OutputPath': '$',
        'Parameters': {
            'ClusterName': 'test-cluster',
            'ClusterTags': [{
                'Key': 'Key1',
                'Value': 'Value1'
            }],
            'ConfigurationName': 'test-configuration',
            'ConfigurationNamespace': 'test',
            'ProfileName': 'test-profile',
            'ProfileNamespace': 'test'
        },
        'Resource': {'Fn::GetAtt': ['testtaskLoadClusterConfiguration518ECBAD', 'Arn'] },
        'ResultPath': '$.ClusterConfiguration',
        'Type': 'Task'
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.LoadClusterConfigurationBuilder.build(
        stack, 'test-task',
        cluster_name='test-cluster',
        cluster_tags=[core.Tag('Key1', 'Value1')],
        profile_namespace='test',
        profile_name='test-profile',
        configuration_namespace='test',
        configuration_name='test-configuration',
    )

    print_and_assert(default_task_json, task)


def test_override_cluster_configs_builder():
    default_task_json = {
        'End': True,
        'Parameters': {
            'ExecutionInput.$': '$$.Execution.Input',
            'ClusterConfiguration.$': '$.ClusterConfiguration.Cluster'
        },
        'OutputPath': '$',
        'Type': 'Task',
        'Resource': {'Fn::GetAtt': ['OverrideClusterConfigsAEEA22C0', 'Arn']},
        'ResultPath': '$.ClusterConfiguration.Cluster'
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.OverrideClusterConfigsBuilder.build(
        stack, 'test-task',
    )

    print_and_assert(default_task_json, task)


def test_fail_if_cluster_running_builder():
    default_task_json = {
        'End': True,
        'Parameters': {
            'ExecutionInput.$': '$$.Execution.Input',
            'DefaultFailIfClusterRunning': True,
            'ClusterConfiguration.$': '$.ClusterConfiguration.Cluster'
        },
        'OutputPath': '$',
        'Type': 'Task',
        'Resource': {'Fn::GetAtt': ['FailIfClusterRunningC0A7FE52', 'Arn']},
        'ResultPath': '$.ClusterConfiguration.Cluster'
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.FailIfClusterRunningBuilder.build(
        stack, 'test-task',
        default_fail_if_cluster_running=True
    )

    print_and_assert(default_task_json, task)


def test_update_cluster_tags_builder():
    default_task_json = {
        'End': True,
        'Parameters': {
            'ExecutionInput.$': '$$.Execution.Input',
            'ClusterConfiguration.$': '$.ClusterConfiguration.Cluster'
        },
        'OutputPath': '$',
        'Type': 'Task',
        'Resource': {'Fn::GetAtt': ['UpdateClusterTags9DD0067C', 'Arn']},
        'ResultPath': '$.ClusterConfiguration.Cluster'
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.UpdateClusterTagsBuilder.build(
        stack, 'test-task',
    )

    print_and_assert(default_task_json, task)


def test_create_cluster_builder():
    default_task_json = {
        'End': True,
        'Parameters': {
            'AdditionalInfo.$': '$.ClusterConfiguration.Cluster.AdditionalInfo',
            'AmiVersion.$': '$.ClusterConfiguration.Cluster.AmiVersion',
            'Applications.$': '$.ClusterConfiguration.Cluster.Applications',
            'AutoScalingRole.$': '$.ClusterConfiguration.Cluster.AutoScalingRole',
            'BootstrapActions.$': '$.ClusterConfiguration.Cluster.BootstrapActions',
            'Configurations.$': '$.ClusterConfiguration.Cluster.Configurations',
            'CustomAmiId.$': '$.ClusterConfiguration.Cluster.CustomAmiId',
            'EbsRootVolumeSize.$': '$.ClusterConfiguration.Cluster.EbsRootVolumeSize',
            'Instances': {
                'AdditionalMasterSecurityGroups.$': '$.ClusterConfiguration.Cluster.Instances.AdditionalMasterSecurityGroups',
                'AdditionalSlaveSecurityGroups.$': '$.ClusterConfiguration.Cluster.Instances.AdditionalSlaveSecurityGroups',
                'Ec2KeyName.$': '$.ClusterConfiguration.Cluster.Instances.Ec2KeyName',
                'Ec2SubnetId.$': '$.ClusterConfiguration.Cluster.Instances.Ec2SubnetId',
                'Ec2SubnetIds.$': '$.ClusterConfiguration.Cluster.Instances.Ec2SubnetIds',
                'EmrManagedMasterSecurityGroup.$': '$.ClusterConfiguration.Cluster.Instances.EmrManagedMasterSecurityGroup',
                'EmrManagedSlaveSecurityGroup.$': '$.ClusterConfiguration.Cluster.Instances.EmrManagedSlaveSecurityGroup',
                'HadoopVersion.$': '$.ClusterConfiguration.Cluster.Instances.HadoopVersion',
                'InstanceCount.$': '$.ClusterConfiguration.Cluster.Instances.InstanceCount',
                'InstanceFleets.$': '$.ClusterConfiguration.Cluster.Instances.InstanceFleets',
                'InstanceGroups.$': '$.ClusterConfiguration.Cluster.Instances.InstanceGroups',
                'KeepJobFlowAliveWhenNoSteps': True,
                'MasterInstanceType.$': '$.ClusterConfiguration.Cluster.Instances.MasterInstanceType',
                'Placement.$': '$.ClusterConfiguration.Cluster.Instances.Placement',
                'ServiceAccessSecurityGroup.$': '$.ClusterConfiguration.Cluster.Instances.ServiceAccessSecurityGroup',
                'SlaveInstanceType.$': '$.ClusterConfiguration.Cluster.Instances.SlaveInstanceType',
                'TerminationProtected.$': '$.ClusterConfiguration.Cluster.Instances.TerminationProtected'
            },
            'JobFlowRole.$': '$.ClusterConfiguration.Cluster.JobFlowRole',
            'KerberosAttributes.$': '$.ClusterConfiguration.Cluster.KerberosAttributes',
            'LogUri.$': '$.ClusterConfiguration.Cluster.LogUri',
            'Name.$': '$.ClusterConfiguration.Cluster.Name',
            'NewSupportedProducts.$': '$.ClusterConfiguration.Cluster.NewSupportedProducts',
            'ReleaseLabel.$': '$.ClusterConfiguration.Cluster.ReleaseLabel',
            'RepoUpgradeOnBoot.$': '$.ClusterConfiguration.Cluster.RepoUpgradeOnBoot',
            'ScaleDownBehavior.$': '$.ClusterConfiguration.Cluster.ScaleDownBehavior',
            'SecurityConfiguration.$': '$.ClusterConfiguration.Cluster.SecurityConfiguration',
            'ServiceRole.$': '$.ClusterConfiguration.Cluster.ServiceRole',
            'StepConcurrencyLevel.$': '$.ClusterConfiguration.Cluster.StepConcurrencyLevel',
            'SupportedProducts.$': '$.ClusterConfiguration.Cluster.SupportedProducts',
            'Tags.$': '$.ClusterConfiguration.Cluster.Tags',
            'VisibleToAllUsers.$': '$.ClusterConfiguration.Cluster.VisibleToAllUsers'
        },
        'Type': 'Task',
        'Resource':
            {'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::elasticmapreduce:createCluster.sync']]}
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.CreateClusterBuilder.build(
        stack, 'test-task',
        roles=emr_profile.EMRRoles(stack, 'test-emr-roles', role_name_prefix='test-roles')
    )

    print_and_assert(default_task_json, task)


def test_run_job_flow_builder():
    default_task_json = {
        'End': True,
        'Parameters': {
            'FunctionName': {
                'Ref': 'RunJobFlow9B18A53F'
            },
            'Payload': {
                'ExecutionInput.$': '$$.Execution.Input',
                'ClusterConfiguration.$': '$.ClusterConfiguration',
                'TaskToken.$': '$$.Task.Token',
                'CheckStatusLambda': {
                    'Fn::GetAtt': ['CheckClusterStatusA7C1019E', 'Arn']
                },
                'RuleName': {
                    'Ref': 'testtaskEventRule9A04A93E'
                },
                'FireAndForget': False
            }
        },
        'Type': 'Task',
        'Resource': {'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::lambda:invoke.waitForTaskToken']]}
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.RunJobFlowBuilder.build(
        stack, 'test-task',
        roles=emr_profile.EMRRoles(stack, 'test-emr-roles', role_name_prefix='test-roles'),
        kerberos_attributes_secret=secretsmanager.Secret(stack, 'test-kerberos-secret'),
        secret_configurations={'Secret': secretsmanager.Secret(stack, 'test-secret-configurations-secret')},
    )

    print_and_assert(default_task_json, task)


def test_add_step_builder():
    default_task_json = {
        'End': True,
        'Parameters': {
            'ClusterId': 'test-cluster-id',
            'Step': {
                'Name': 'test-step',
                'ActionOnFailure': 'CONTINUE',
                'HadoopJarStep': {
                    'Jar': 'Jar',
                    'MainClass': 'Main',
                    'Args': ['Arg1', 'Arg2'],
                    'Properties': []
                }
            }
        },
        'Type': 'Task',
        'Resource': {'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::elasticmapreduce:addStep.sync']]}
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.AddStepBuilder.build(
        stack, 'test-task',
        cluster_id='test-cluster-id',
        emr_step=emr_code.EMRStep('test-step', 'Jar', 'Main', ['Arg1', 'Arg2']),
    )

    print_and_assert(default_task_json, task)


def test_terminate_cluster_builder():
    default_task_json = {
        'End': True,
        'Parameters': {
            'ClusterId': 'test-cluster-id'
        },
        'Type': 'Task',
        'Resource':
            {'Fn::Join': ['', ['arn:', {'Ref': 'AWS::Partition'}, ':states:::elasticmapreduce:terminateCluster.sync']]}
    }

    stack = core.Stack(core.App(), 'test-stack')

    task = emr_tasks.TerminateClusterBuilder.build(
        stack, 'test-task',
        name='test-terminate-task',
        cluster_id='test-cluster-id',
    )

    print_and_assert(default_task_json, task)
