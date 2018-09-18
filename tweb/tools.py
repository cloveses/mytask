from models.model import *
import settings

# @db_session
# def init_secrity_qstn():
#     if not exists(s for s in SsQuestion):
#         for group,qstns in enumerate(settings.SECRITY_QUESTION):
#             for qstn in qstns:
#                 SsQuestion(question=qstn,group=group)