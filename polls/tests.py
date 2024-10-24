from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for pub_date in future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for pub_date one day or older
        """
        time = time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns true for pub_date is less than one day
        """
        time = time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

def create_question(question_text, days):

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text= question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    
    def test_past_question(self):
        question = create_question(question_text="Past question", days= -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )
    
    def test_future_question(self):
        create_question(question_text="Future question", days= 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )
    def test_future_and_past_questions(self):
        question = create_question(question_text="Past question", days= -30)
        create_question(question_text="Future question", days= 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )
    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1", days= -30)
        question2 = create_question(question_text="Past question 2", days= -1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2,question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question 1", days= 30)
        response = self.client.get(reverse("polls:details", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Future question 1", days= -30)
        response = self.client.get(reverse("polls:details", args=(past_question.id,)))
        self.assertContains(response, test_past_question.question_text)