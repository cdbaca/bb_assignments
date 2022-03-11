/*
Query attributes: Course pk, course content title, course content parent_id (if exists), course_id, term name
Notes: This will pull all courses
a) with a specific suffix (e.g., _SU22) and
b) in a set of courses from a term or terms (courses like "Distance", "Online", etc.)
*/
select
cm.pk1
,cc.title
,cc.parentId
,course_id
,t.name
from course_main cm
	inner join course_term ct on ct.crsmain_pk1 = cm.pk1
	inner join term t on t.pk1 = ct.term_pk1
	left join (
				select
				crsmain_pk1
				,concat('_', cc.pk1, '_1') as parentId
				,cc.title
				from course_contents cc
				where (cc.title = 'Course Content' and cc.position in (0, 1))
					or (cc.title like '%VISTA%') -- find courses that have a 'Course Content' folder labeled incorrectly
	) cc on cc.crsmain_pk1 = cm.pk1
where cm.course_id like '%SU22%'
	and cm.pk1 not in (select crsmain_pk1 from course_course)
	and t.name similar to '%(Distance|SOM|Online|Rhema|Doctoral)%'
order by cm.course_id