# =============================================================================
# ECS Cluster
# =============================================================================

resource "aws_ecs_cluster" "main" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${local.name_prefix}-cluster"
  }
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = "FARGATE"
  }
}

# =============================================================================
# ECS Task Definition
# =============================================================================

resource "aws_ecs_task_definition" "main" {
  family                   = "${local.name_prefix}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.container_cpu
  memory                   = var.container_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name  = var.project_name
      image = "${aws_ecr_repository.main.repository_url}:${var.docker_image_tag}"
      
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "STREAMLIT_SERVER_PORT"
          value = tostring(var.container_port)
        },
        {
          name  = "STREAMLIT_SERVER_ADDRESS"
          value = "0.0.0.0"
        },
        {
          name  = "STREAMLIT_BROWSER_GATHER_USAGE_STATS"
          value = "false"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.main.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:${var.container_port}/_stcore/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }

      essential = true
    }
  ])

  tags = {
    Name = "${local.name_prefix}-task-definition"
  }
}

# =============================================================================
# ECS Service
# =============================================================================

resource "aws_ecs_service" "main" {
  name                               = "${local.name_prefix}-service"
  cluster                            = aws_ecs_cluster.main.id
  task_definition                    = aws_ecs_task_definition.main.arn
  desired_count                      = var.desired_count
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200
  launch_type                        = "FARGATE"
  scheduling_strategy                = "REPLICA"
  platform_version                   = "LATEST"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.main.arn
    container_name   = var.project_name
    container_port   = var.container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  depends_on = [
    aws_lb_listener.http,
    aws_iam_role_policy_attachment.ecs_execution
  ]

  tags = {
    Name = "${local.name_prefix}-service"
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}
