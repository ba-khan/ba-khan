SELECT 
			  bakhanapp_assesment_skill.id_skill_name_id
			FROM 
			  public.bakhanapp_assesment_config, 
			  public.bakhanapp_assesment_skill
			WHERE 
			  bakhanapp_assesment_config.id_assesment_config = bakhanapp_assesment_skill.id_assesment_config_id AND  
			  bakhanapp_assesment_config.id_assesment_config = 1


SELECT 
  bakhanapp_student_skill.kaid_student_id, 
  bakhanapp_skill_progress.to_level, 
  bakhanapp_skill_progress.date, 
  bakhanapp_student_skill.id_skill_name_id
FROM 
  public.bakhanapp_student_skill, 
  public.bakhanapp_skill_progress
WHERE 
  bakhanapp_student_skill.id_student_skill = bakhanapp_skill_progress.id_student_skill_id AND
  bakhanapp_student_skill.kaid_student_id = 'kaid_1097501097555535353578558' and
  bakhanapp_student_skill.id_skill_name_id IN (SELECT 
			  bakhanapp_assesment_skill.id_skill_name_id
			FROM 
			  public.bakhanapp_assesment_config, 
			  public.bakhanapp_assesment_skill
			WHERE 
			  bakhanapp_assesment_config.id_assesment_config = bakhanapp_assesment_skill.id_assesment_config_id AND  
			  bakhanapp_assesment_config.id_assesment_config IN (SELECT id_assesment_conf_id FROM public.bakhanapp_assesment where end_date ='2016-02-03'))
  
ORDER BY
  bakhanapp_student_skill.id_skill_name_id ASC;
