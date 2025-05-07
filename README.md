# Système de Bots Discord en Python

Bienvenue dans mon projet de **système de bots Discord entièrement libre et modifiable** !  
Ce projet te permet de **gérer plusieurs bots Discord simultanément** à partir d’une base unique, tout en restant **simple**, **flexible** et **entièrement personnalisable**.

---

## ✨ Fonctionnalités principales

- **Multi-bots** : Lance et gère plusieurs bots Discord en même temps.
- **Système modulaire** : Ajoute facilement des **modules** pour enrichir les fonctionnalités.
- **Commandes personnalisables** : Crée, modifie ou supprime des commandes selon tes besoins.
- **Installation automatique** des dépendances au lancement du programme.
- **Configuration simple via un CLI dédié** entièrement modifiable.
- **100% Python** : Code clair, léger et adapté à tous les niveaux.

---

## 📦 Installation

1. **Clone le dépôt :**
   ```bash
   git clone https://github.com/Romaindu74/Bot-V2.git
   cd Bot-V2
   ```

2. **Lance directement le programme :**
   ```bash
   python main.py
   ```
   > Les dépendances nécessaires seront installées automatiquement si elles ne sont pas déjà présentes.

3. **Configure tes bots via le CLI intégré** :
   - Ajoute, modifie ou supprime tes bots facilement depuis une interface en ligne de commande.
   - Aucune modification manuelle de fichiers nécessaire !

---

## ⚙️ Configuration

La configuration des bots se fait **directement depuis le CLI** inclus dans le projet.  
Le CLI permet :
- D’ajouter de nouveaux bots en saisissant leur token, préfixe, et modules utilisés.
- De modifier les paramètres existants.
- De supprimer ou désactiver des bots facilement.

Le CLI est également **modulaire** et **modifiable** selon tes besoins.

---

## 🛠️ Ajouter un module

1. Crée un fichier Python dans le dossier `/Slazhe/Discord/Files/`.
2. Suis la structure de base d’un module :
   ```python
   from discord.ext    import commands
   from Slazhe.Discord import Cog, command, Context

   class Ping(Cog):
      def __init__(self, bot):
         self.bot: commands.Bot = bot.bot

      @command(name="ping", description="Vérifie la latence")
      async def ping(self, ctx: Context):
          latency = round(self.bot.latency * 1000)
        
          await ctx.send(f"Pong! {latency}ms", reference=ctx.ctx.message)

   async def setup(bot):
      return bot.add_cog(Ping(bot))
   ```
---

## 📄 Licence

Ce projet est distribué sous la licence suivante :

- **Utilisation, modification et redistribution autorisées uniquement à des fins non commerciales.**
- Toute utilisation commerciale est interdite sans autorisation explicite.

Pour plus de détails, consulte le fichier [`LICENSE`](./LICENSE).

---

## 🚀 Objectif

L’objectif de ce projet est de **simplifier et accélérer** le développement de bots Discord, en proposant un système **modulaire**, **ouvert**, et **très personnalisable**, sans contraintes techniques lourdes.

---

## 🙌 Contribuer

Toute contribution est la bienvenue !  
Tu peux :
- Proposer de nouvelles fonctionnalités.
- Créer et partager des modules.
- Corriger des bugs ou améliorer la base existante.

**N'hésite pas à ouvrir une issue ou à proposer une pull request !**

---

## 📫 Contact

Si tu as des questions, suggestions ou besoins d’aide :
- **Discord** : Slazhe
- **Email** : romain@slazhe.com

---

# Merci d'utiliser ce projet ! 🚀
