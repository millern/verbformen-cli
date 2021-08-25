import verbformen_cli.clients as clients
import verbformen_cli.models as models
import verbformen_cli.display as display

Client = clients.VerbformenClient
PageResult = models.PageResult
PartOfSpeech = models.PartOfSpeech
Definition = models.Definition
Noun = models.Noun
Verb = models.Verb
Adjective = models.Adjective
NotFound = models.NotFound
display_summary = display.display_summary

__version__ = "0.1.0"
