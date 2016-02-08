SELECT 
			  bakhanapp_assesment_skill.id_skill_name_id
			FROM 
			  public.bakhanapp_assesment_config, 
			  public.bakhanapp_assesment_skill
			WHERE 
			  bakhanapp_assesment_config.id_assesment_config = bakhanapp_assesment_skill.id_assesment_config_id AND  
			  bakhanapp_assesment_config.id_assesment_config = 1

###############################################################
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


################################################################
SELECT 
  bakhanapp_student_skill.kaid_student_id, 
  bakhanapp_skill_progress.to_level,
  bakhanapp_skill_progress.date, 
  bakhanapp_student_skill.id_skill_name_id
FROM 
  public.bakhanapp_student_skill, 
  public.bakhanapp_skill_progress
WHERE 
  bakhanapp_student_skupdate public.bakhanapp_grade set performance_points =0 ; ill.id_student_skill = bakhanapp_skill_progress.id_student_skill_id AND
  bakhanapp_student_skill.kaid_student_id = 'kaid_1097501097555535353578558' AND 
  bakhanapp_student_skill.id_skill_name_id = '12293397'
ORDER BY
  bakhanapp_student_skill.id_skill_name_id ASC;

####################################################################
update public.bakhanapp_grade set performance_points =20 where id_grade = 197; 

#####################################################################
update public.bakhanapp_tutor set email ='tutorbakhan@yopmail.com' ;

########################################################################  
SELECT 
  bakhanapp_student.name AS name_student, 
  bakhanapp_student.email AS email_student, 
  bakhanapp_tutor.name AS name_tutor, 
  bakhanapp_tutor.email AS email_tutor, 
  bakhanapp_grade.id_grade, 
  bakhanapp_grade.grade, 
  bakhanapp_grade.kaid_student_id
FROM 
  public.bakhanapp_grade, 
  public.bakhanapp_student, 
  public.bakhanapp_tutor
WHERE 
  bakhanapp_grade.kaid_student_id = bakhanapp_student.kaid_student AND
  bakhanapp_grade.kaid_student_id = bakhanapp_tutor.kaid_student_child_id and
  bakhanapp_grade.id_assesment_id = 67;

########################################################################
SELECT 
  bakhanapp_assesment_skill.id_assesment_config_id, 
  bakhanapp_assesment_skill.id_skill_name_id, 
  bakhanapp_skill.name_spanish AS name
FROM 
  public.bakhanapp_assesment_skill, 
  public.bakhanapp_skill
WHERE 
  bakhanapp_assesment_skill.id_skill_name_id = bakhanapp_skill.id_skill_name;

##########################################################################
SELECT 
  bakhanapp_grade.kaid_student_id, 
  sum(bakhanapp_video_playing.seconds_watched) 
FROM 
  public.bakhanapp_grade, 
  public.bakhanapp_video_playing
WHERE 
  bakhanapp_grade.kaid_student_id = bakhanapp_video_playing.kaid_student_id AND
  bakhanapp_grade.id_assesment_id = 181
group by bakhanapp_grade.kaid_student_id;

##############################################################################
SELECT 
  bakhanapp_grade.kaid_student_id, 
  sum(bakhanapp_video_playing.seconds_watched) 
FROM 
  public.bakhanapp_grade, 
  public.bakhanapp_video_playing
WHERE 
  bakhanapp_grade.kaid_student_id = bakhanapp_video_playing.kaid_student_id AND
  bakhanapp_grade.id_assesment_id = 181 AND 
  bakhanapp_video_playing.date >= '2016-01-01' 
GROUP BY 
  bakhanapp_grade.kaid_student_id;
