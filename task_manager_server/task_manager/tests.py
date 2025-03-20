from rest_framework import status
from rest_framework.test import APITestCase

from task_manager.models import Label, Project, Status, User, Issue


def create_issue(project, status):
    return Issue.objects.create(
        project=project,
        issue_type=Issue.IssueTypes.TASK,
        summary='Test issue',
        priority=Issue.Priorities.MEDIUM,
        status=status,
        serial_number=1,
    )


class IssueViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')
        self.project = Project.objects.create(project_key='TEST', owner=self.user)
        self.status = Status.objects.create(project=self.project, name='TODO')
        self.label = Label.objects.create(project=self.project, name='TEST')

    # def tearDown(self):
    #     self.user.delete()
    #     self.label.delete()
    #     self.status.delete()
    #     self.project.delete()
 
    def test_create_issue(self):
        data = {
            'project_id': self.project.project_id,
            'issue_type': Issue.IssueTypes.TASK,
            'summary': 'Test issue',
            'description': 'Test description',
            'assignee_id': self.user.user_id,
            'priority': Issue.Priorities.MEDIUM,
            'status_id': self.status.status_id,
            'start_date': '2025-01-01',
            'due_date': '2025-12-31',
            'label_ids': [self.label.label_id],
        }

        response = self.client.post('/api/issue/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['issue_id'], 1)
        self.assertEqual(response.data['project'], data['project_id'])
        self.assertEqual(response.data['summary'], data['summary'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['issue_type'], data['issue_type'])
        self.assertEqual(response.data['priority'], 
                         {'code': data['priority'], 'name': Issue.Priorities(data['priority']).name.capitalize()})
        self.assertEqual(response.data['status'],
                         {'status_id': self.status.status_id, 'name': self.status.name})
        self.assertEqual(response.data['start_date'], data['start_date'])
        self.assertEqual(response.data['due_date'], data['due_date'])
        self.assertEqual(response.data['assignee'], 
                         {'user_id': self.user.user_id, 'username': self.user.username, 'email': self.user.email, 'avatar': self.user.avatar})
        self.assertEqual(response.data['labels'], 
                         [{'label_id': self.label.label_id, 'name': self.label.name}])
        self.assertEqual(response.data['serial_number'], 1)
        self.assertTrue(response.data['created_at'])
        self.assertTrue(response.data['updated_at'])
        self.assertEqual(response.data['parent'], None)

    def test_list_issues(self):
        create_issue(self.project, self.status)
        create_issue(self.project, self.status)

        response = self.client.get('/api/issue/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_issue(self):
        issue = create_issue(self.project, self.status)

        response = self.client.get(f'/api/issue/{issue.issue_id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['issue_id'], issue.issue_id)

    def test_update_issue(self):
        issue = create_issue(self.project, self.status)
        new_data = {'summary': 'Updated summary'}

        response = self.client.patch(f'/api/issue/{issue.issue_id}', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], new_data['summary'])

    def test_delete_issue(self):
        issue = create_issue(self.project, self.status)

        response = self.client.delete(f'/api/issue/{issue.issue_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)