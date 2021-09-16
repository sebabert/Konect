from __future__ import print_function
from mailmerge import MailMerge
from json import loads


def fill_cvmodel(source, formatcv, data, cvid):

	if source and data and formatcv:
		template = "cv_"+formatcv+"_modele.docx"
		document = MailMerge(template)

		if source == "es":
			document.merge(
				name=data['name'] if "name" in data else "--",
				status=data['status'] if "status" in data else "--",
				job=data['job'] if "job" in data else "--",
				phone=data['phone'] if "phone" in data else "--",
				mobility=data['mobility'] if "mobility" in data else "--",
				address=data['address'] if "address" in data else "--",
				availability=data['availability'] if "availability" in data else "--",
				skills=data['skills'] if "skills" in data else "",
				experience=data['experience'] if "experience" in data else "",
				price=data['price'] if "price" in data else "--",
				email=data['email'] if "email" in data else "--"
			)

			if "formations" in data:
				if data['formations'] and data['formations'] != ' ' and data['formations'] is not None:
					data_edu = loads(data['formations'])
					if data_edu:
						diplomas = []
						for education in data_edu:
							diplomas.append({
								'diploma.date': education['date'],
								'diploma.name': education['name']
							})
				else:
					diplomas = []
				document.merge_rows('diploma.year', diplomas)

			if "experience" in data:
				if data['experience'] and data['experience'] != ' ' and data['experience'] is not None:
					data_exp = loads(data['experience'])
					if data_exp:
						experience = []
						for xp in data_exp:
							experience.append({
								'job.date': xp['duration'],
								'job.title': xp['job_title'],
								'job.company': xp['company_name'],
								'job.location': xp['job_location'],
								'job.description': xp['description'],
								'job.tools': xp['tools']
							})
				else:
					experience = []
				document.merge_rows('job.date', experience)

			formatted_cv = formatcv+'_'+data['name']+'_'+cvid+'.docx'
			document.write(formatted_cv)
			return formatted_cv

		elif source == "db":
			candidate = data["candidate"]
			skills_queryset = list(data['skills'])
			experiences_queryset = list(data['experiences'])
			educations_queryset = list(data['educations'])

			skills = ""
			first_skill = True
			for skill in skills_queryset:
				if first_skill:
					skills += skill.name
					first_skill = False
				else:
					skills += " - "+skill.name

			document.merge(
				name=candidate.name if candidate.name else "--",
				status=candidate.status if candidate.status else "--",
				job=candidate.job if candidate.job else "--",
				phone=candidate.phone if candidate.phone else "--",
				mobility=candidate.mobility if candidate.mobility else "--",
				address=candidate.address if candidate.address else "--",
				availability=candidate.availability if candidate.availability else "--",
				price=candidate.price if candidate.price else "--",
				email=candidate.email if candidate.email else "--",
				salary=candidate.salary if candidate.salary else "--",
				skills=skills if skills else "--",
			)

			diplomas = []
			for education in educations_queryset:
				diplomas.append({
					'diploma.year': education.date,
					'diploma.name': education.name
				})

			experience = []
			for xp in experiences_queryset:
				experience.append({
					'job.date': xp.duration,
					'job.title': xp.job_title,
					'job.company': xp.company_name,
					'job.location': xp.job_location,
					'job.description': xp.description,
					'job.tools': xp.tools
				})

			document.merge_rows('diploma.year', diplomas)
			document.merge_rows('job.date', experience)

			formatted_cv = formatcv+'_'+candidate.name+'_'+cvid+'.docx'
			document.write(formatted_cv)
			return formatted_cv
	else:
		return ""
