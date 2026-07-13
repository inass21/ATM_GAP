from django.test import TestCase
from django.urls import reverse

from .models import Fournisseur, GAB


class DiagnosticPageTests(TestCase):
    def setUp(self):
        self.fournisseur = Fournisseur.objects.create(
            id_fournisseur=1,
            nom_fournisseur="NCR",
        )
        self.gab = GAB.objects.create(
            terminal=100000003,
            nom_gab="Agence Massira",
            libelle_agence="Agence Massira",
            ville="Casablanca",
            ip_adresse_gab="10.45.2.140",
            numero_serie="SN-123",
            fournisseur=self.fournisseur,
            etat=GAB.ETAT_HORS_SERVICE,
        )

    def test_diagnostic_page_renders_with_context(self):
        response = self.client.get(reverse("gab:diagnostic", kwargs={"gab_id": self.gab.terminal}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diagnostic GAB")
        self.assertContains(response, self.gab.nom_gab)
        self.assertContains(response, "État des composants")
