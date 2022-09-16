


def add_course_to_class(classID,courseID,numberOfCourse):
    numberOfCourse=0
    course=Course.objects.get(id=courseID)
    classes= Class.objects.get(id=classID)
    try: 
      courseinclass= CourseInClass.objects.get(courseID=course.id,classID=classes.id)
      if courseinclass is None:
        numberOfCourse +=1
        courseinclass2=CourseInClass.objects.create(classID=classes,courseID=course,numberOfCourse=numberOfCourse)
        courseinclass2.save()
      else:
        pass
    except CourseInClass.DoesNotExist:
      numberOfCourse += 1
      courseinclass2=CourseInClass.objects.create(classID=classes,courseID=course,numberOfCourse=numberOfCourse)
      courseinclass2.save()