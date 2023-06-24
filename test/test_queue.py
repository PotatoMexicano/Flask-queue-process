import unittest
from queue_tool.model import Job
from uuid import uuid4
from datetime import datetime

class Test(unittest.TestCase):

    def test_class_job(self):

        uuid = uuid4().hex
        job = Job({'hash': uuid, 'item': 'Teste#02', 'valor': 1})

        self.assertIsInstance(job, Job)

        self.assertEqual(job.hash, uuid)
        self.assertEqual(job.item, 'Teste#02')
        self.assertEqual(job.valor, 1)
    
    def test_type_attr_job(self):
        
        job = Job({'hash': uuid4().hex, 'item': 'Teste#02', 'valor': 1})
        
        self.assertIsInstance(job.valor, int)
        self.assertIsInstance(job.hash, str)
        self.assertIsInstance(job.item, str)
    
    def test_status_job(self):
        
        job = Job({'hash': uuid4().hex, 'item': 'Teste#02', 'valor': 1})
        status = 'Em processamento'
        
        self.assertEqual(job.status, status)
        
    def test_dict_job(self):
        
        job = Job({'hash': uuid4().hex, 'item': 'Teste#02', 'valor': 1})
        job = job.as_dict()
        
        dikti = {
            'item': 'Teste#02',
            'valor': 1,
            'status': 'Em processamento',
        }
        
        self.assertEqual(job, dikti)
