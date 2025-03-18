from aws_cdk import (
    App,
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elb,
    aws_applicationautoscaling as appscaling,
    Duration  
)

class MyEcsStack(Stack):
    def __init__(self, scope: App, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a VPC with 2 availability zones
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Create an ECS cluster in the VPC
        cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)

        # Reference the existing ECR repository
        repository = ecr.Repository.from_repository_name(self, "MyFastAPIRepository", "my-fastapi-app")

        # Create an IAM role for ECS task
        task_role = iam.Role(
            self, "TaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )

        # Create a Fargate Task Definition
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef", memory_limit_mib=512, cpu=256, task_role=task_role)

        # Add a container definition to the task
        container = task_definition.add_container(
            "AppContainer",
            image=ecs.ContainerImage.from_ecr_repository(repository),  # Image from ECR repository
            memory_limit_mib=512,
            cpu=256
        )
        
        # Define the port mappings
        container.add_port_mappings(
            ecs.PortMapping(container_port=8000)  # Exposing port 8000
        )

        # Create an Application Load Balancer
        lb = elb.ApplicationLoadBalancer(self, "MyLoadBalancer", vpc=vpc, internet_facing=True)

        # Add a listener for HTTP traffic (port 80)
        listener = lb.add_listener("Listener", port=80)

        # Create a target group for the ECS service
        target_group = listener.add_targets(
            "EcsTargets",
            port=80,
            targets=[],
            health_check={
            'path': '/health',  # Use '/health' instead of '/'
        
            }
        )

        # Create a Fargate service
        ecs_service = ecs.FargateService(self, "FargateService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,  # Ensure at least one replica is running
            assign_public_ip=True  # Assign public IPs to the task (so it can be accessed)
        )

        # Register the ECS service with the load balancer
        target_group.add_target(ecs_service)
        
        # Enable auto-scaling for the ECS service
        scaling = ecs_service.auto_scale_task_count(
            min_capacity=1,  # Minimum number of tasks 
            max_capacity=10  # Maximum number of tasks
        )

        # Add a scaling policy based on CPU utilization
        scaling.scale_on_cpu_utilization(
            "CpuScalingPolicy",  
            target_utilization_percent=70,  # Target CPU utilization
            scale_in_cooldown=Duration.seconds(60),  # Wait time before scaling in
            scale_out_cooldown=Duration.seconds(60)  # Wait time before scaling out
        )

        # Output the load balancer URL
        CfnOutput(self, "LoadBalancerURL", value=lb.load_balancer_dns_name)

# Create the app and stack
app = App()
MyEcsStack(app, "MyEcsStack")
app.synth()
