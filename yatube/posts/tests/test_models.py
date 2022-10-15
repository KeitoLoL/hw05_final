from .input_data_for_tests import InputDataClass


class PostModelTest(InputDataClass):

    def test_models_have_correct_object_names(self):
        self.assertEqual(str(self.group), self.group.title)
        self.assertEqual(str(self.post), self.post.text[:15])
