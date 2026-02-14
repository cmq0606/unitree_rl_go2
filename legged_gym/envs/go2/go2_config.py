from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class GO2RoughCfg( LeggedRobotCfg ):
    class env(LeggedRobotCfg.env):
        num_envs = 16
    class terrain(LeggedRobotCfg.terrain):
        mesh_type = 'plane'
        curriculum = False
    class commands(LeggedRobotCfg.commands):
        curriculum = False
        num_commands = 4   # 改成 4
        ranges = {
            'lin_vel_x': [0.4, 0.4],
            'lin_vel_y': [0.0, 0.0],
            'ang_vel_yaw': [0.0, 0.0],
            'heading': [0.0, 0.0],   # 新增
        }





    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.42] # x,y,z [m]
        default_joint_angles = { # = target angles [rad] when action = 0.0
            'FL_hip_joint': 0.1,   # [rad]
            'RL_hip_joint': 0.1,   # [rad]
            'FR_hip_joint': -0.1 ,  # [rad]
            'RR_hip_joint': -0.1,   # [rad]

            'FL_thigh_joint': 0.8,     # [rad]
            'RL_thigh_joint': 1.,   # [rad]
            'FR_thigh_joint': 0.8,     # [rad]
            'RR_thigh_joint': 1.,   # [rad]

            'FL_calf_joint': -1.5,   # [rad]
            'RL_calf_joint': -1.5,    # [rad]
            'FR_calf_joint': -1.5,  # [rad]
            'RR_calf_joint': -1.5,    # [rad]
        }

    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {'joint': 40.0}  # [N*m/rad]
        # 提高关节刚度
        damping = {'joint': 1.5}     # [N*m*s/rad]# 增加阻尼
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.10    # 再小一点，让动作更平滑
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4

    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/go2/urdf/go2.urdf'
        name = "go2"
        foot_name = "foot"
        penalize_contacts_on = ["thigh", "calf"]
        terminate_after_contacts_on = ["base"]
        self_collisions = 1 # 1 to disable, 0 to enable...bitwise filter
  
    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9
        base_height_target = 0.25
        class scales( LeggedRobotCfg.rewards.scales ):
            # === 行走主奖励 ===
            tracking_lin_vel = 6.0  #增大前进奖励

            # === 稳定性约束 ===
            orientation = -6.0  #提高姿态惩罚
            lin_vel_z = -5.0    #提高上下跳惩罚
            ang_vel_xy = -0.07

            # === 抑制乱摆 ===
            dof_vel = -0.005
            torques = -0.0002
            dof_pos_limits = -10.0
            
            #action_rate = -0.01


class GO2RoughCfgPPO( LeggedRobotCfgPPO ):
    obs_groups = {
        "policy": ["obs"],
        "critic": ["obs"]
    }
    policy = {
        "class_name": "PPO",  # 指定PPO算法
        "actor_obs_normalization": True,  # 设置是否标准化actor的观察
        "critic_obs_normalization": True,  # 设置是否标准化critic的观察
    }
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.002
    class runner( LeggedRobotCfgPPO.runner ):
        run_name = ''
        experiment_name = 'rough_go2'
        max_iterations = 3000
        save_interval = 100
  
