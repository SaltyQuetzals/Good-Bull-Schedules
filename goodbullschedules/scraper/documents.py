from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer, tokenizer
from scraper import models

course = Index("course")

course.settings(number_of_shards=1, number_of_replicas=0)

shingle_analyzer = analyzer(
    "gram_analyzer",
    tokenizer="standard",
    filter=["lowercase", "stop", "shingle"],
)


@course.doc_type
class CourseDocument(DocType):

    search = fields.TextField(analyzer=shingle_analyzer)
    abbrev = fields.TextField()

    def prepare_search(self, instance):
        description = ""
        if instance.description:
            description = instance.description.strip()
        return " ".join(
            [instance.dept, instance.course_num, instance.name, description]
        )

    def prepare_abbrev(self, instance):
        return f"{instance.dept} {instance.course_num}"

    class Meta:
        model = models.Course

        fields = ["name", "dept", "course_num", "description"]
