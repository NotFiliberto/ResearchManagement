#Add a researcher with user.id
user = User.query.filter_by(email="vineet.cesca@gmail.com").first()
        new_res = Researcher.query.filter_by(id=user.id).all()
        db.session.add(new_res)
        db.session.commit()

#delete a researcher (all)
delete_res = Researcher.query.all()
db.session.delete(delete_res)
db.session.commit()

#Notice, researchers/evaluators must be created first and then
# check if they are logged as users
researcher = Researcher(username="Vin1", password="1234", email="vin1@gmail.com")
db.session.add(researcher)
db.session.commit()

user = User.query.filter_by(username="vinDude")



#tester

 print("SEPARATOR")
        print(User.query.filter_by(email="vineet.cesca@gmail.com").first())
        print(Researcher.query.filter_by(id=user.id).all())
        # authentication
        
        users = User.query.all()
        print(user.id)
        print("users here:")
        print(User.query.all())
        for u in users:
            print(u.id)
            print(u.email)     
            print(u.username)
            print(u.password) 
        
        
        researchers = Researcher.query.all()
        print("researchers here:")
        print(Researcher.query.all())
        for u in researchers:
            print(u.id)
            print(u.email)     
            print(u.username)
            print(u.password) 

        evaluators = Evaluator.query.all()
        print("evaluators here:")
        print(Evaluator.query.all())
        for u in evaluators:
            print(u.id)
            print(u.email)     
            print(u.username)
            print(u.password) 

        researcher = Researcher.query.filter_by(id=user.id)
        evaluator = Evaluator.query.filter_by(id=user.id)
        print(researcher)
        print(evaluator)
        print("sus")