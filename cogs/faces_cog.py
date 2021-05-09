"""
File: faces_cog.py
makes mashed up faces
Contributors: Karl Miller
Created: 5/8/2021
Updated: 5/8/2021
"""

import requests, random, io, discord, os
from discord.ext import commands  # required for method and cog decoration
from PIL import Image, ImageEnhance
import numpy as np


class FacesCog(commands.Cog):
    """
    Main purpose of this Cog is to generate mashed up faces.

    It selects a random face from the source faces and uses that as its color basis.

    Then it randomly selects images for each mask portion, and pastes them together to make a new face, recoloring
     to match the color basis as it goes.

    Finally, it sends the new mashup face to the Discord chat.

    It also does a few image manipulation things on images uploaded to chat in a message.

    """
    def __init__(self, client):
        self.client = client
        self.directory = "faces-assets"
        """
        The directory where image assets are stored. Should /masks and /faces subdirectories
        """
        self.tmp = f"{self.directory}/tmp.png"

    @commands.command(pass_context=True)
    async def get_face(self, ctx):
        """
        Generates a new mashed-up face and sends it to the Discord chat.
        :param ctx: Discord Context
        """
        fm = FaceMasher(f"{self.directory}/masks", f"{self.directory}/faces")
        mashup = fm.get_mashup()
        mashup.save(self.tmp)
        await ctx.send(file=discord.File(self.tmp))

    @commands.command(pass_context=True)
    async def quantize(self, ctx, msg_content):
        """
        'Quantizes' and image sent in the Discord chat. This reduces the colors in the image to the number specified.

        I.e. !quantize 10 will reduce an image to 10 colors.

        Max number is 256.

        :param ctx: Message context
        :param msg_content: Message content, should have an integer between 1 and 256.
        """
        try:
            quant = int(msg_content)
        except ValueError:
            await ctx.send("Invalid input - must be number")
            return
        if quant > 256 or quant < 0:
            await ctx.send("Invalid input - must be between 0 and 256")
            return
        img = await self.get_attached_images(ctx)  # gets images from context
        if not img:
            return
        img = img[0].quantize(colors=int(msg_content))
        img.save(self.tmp)
        await ctx.send(file=discord.File(self.tmp))

    @commands.command(pass_context=True)
    async def get_channel(self, ctx, msg_content='x'):
        """
        Gets an image color channel, R, G, or B

        :param ctx: Discord Context
        :param msg_content:
        :type msg_content: str
        """
        images = await self.get_attached_images(ctx)
        if images:
            msg = ''
            channel_names = ['r','g','b']
            choice = msg_content.lower()
            if choice not in channel_names:
                msg += 'invalid channel, showing red'
                channel_num = 0
            else:
                channel_num = channel_names.index(choice)
                for img in images:
                    chans = []
                    for i in range(0, len(channel_names)):
                        if i == channel_num:
                            selected = img.getchannel(i)
                        else:
                            selected = Image.new("L", img.size)
                        chans.append(selected)
                    out = Image.merge("RGB", (chans[0],chans[1],chans[2]))
                    out.save(f"{self.tmp}")
                    await ctx.send(msg, file=discord.File(self.tmp))

    async def get_attached_images(self, ctx):
        """
        Gets a Images user has attached. Will print error message if Image needs to be attached.

        Returns NONE if there is no image to be found.

        Returns Array of PIL.Image if multiple images are found.

        :param ctx: The Discord message context
        :return: List of PIL.Image or None
        """
        if not ctx.message.attachments or len(ctx.message.attachments) == 0:
            await ctx.send("Attach Image to function")
            return None
        images = []
        for i in range(0, len(ctx.message.attachments)):
            attachment_url = ctx.message.attachments[i].url
            file_request = requests.get(attachment_url)
            bytes_io = io.BytesIO(file_request.content)
            with open(f'{self.directory}/tmp.png', 'wb') as f:
                f.write(bytes_io.read())
            img = Image.open(f'{self.directory}/tmp.png')
            images.append(img)
        return images


def setup(client):
    """
    Set's up the cog, required fr cogs
    :return:
    """
    client.add_cog(FacesCog(client))


class Mask:
    def __init__(self, mask_img):
        """
        Holds a mask image. Crops out the masked portion of target image passed to it.
        """
        self.mask = mask_img

    def get_cropped(self, target_img):
        """
        Returns a new image consisting of target_img cropped to the mask area.

        :param target_img: Image to crop
        :return: new Image
        """
        new = Image.new("RGB", target_img.size)
        new.paste(target_img, self.mask)
        return new


class FaceMasher:
    def __init__(self, mask_directory, face_directory):
        """
        Generates mashed up images using files in parameter directories.

        :param mask_directory: relative directory string
        :param face_directory: relative directory string
        """
        file_list = os.listdir(mask_directory)
        self.masks = {}
        for filename in file_list:
            img = Image.open(f"{mask_directory}/{filename}")
            self.masks[filename] = Mask(img)
        self.source_images = []
        file_list = os.listdir(face_directory)
        for filename in file_list:
            self.source_images.append(Image.open(f"{face_directory}/{filename}"))


    def get_mashup(self):
        """
        Gets a new mashup

        :return: Pillow Image
        """
        color_source = self.source_images[random.randint(0, len(self.source_images) - 1)]
        tmp_sources = []
        for raw_img in self.source_images:
            tmp_sources.append(FaceMasher.match_bands(raw_img, color_source))
        mashup = Image.new("RGB", color_source.size)
        for key in self.masks.keys():
            a_mask = self.masks[key]
            rand_source = tmp_sources[random.randint(0, len(tmp_sources) - 1)]
            a_crop = a_mask.get_cropped(rand_source)
            mashup.paste(a_crop, a_mask.mask)
        enhancer = ImageEnhance.Brightness(mashup)
        mashup = enhancer.enhance(2.5)
        return mashup

    @staticmethod
    def hist_norm(source, template):
        """
        Matches two histograms

        :param source: image to change
        :param template: image to use as template colors
        :return: numpy array that can be converted to an image
        """
        # found on github

        olddtype = source.dtype
        oldshape = source.shape
        source = source.ravel()
        template = template.ravel()

        s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                                return_counts=True)
        t_values, t_counts = np.unique(template, return_counts=True)
        s_quantiles = np.cumsum(s_counts).astype(np.float64)
        s_quantiles /= s_quantiles[-1]
        t_quantiles = np.cumsum(t_counts).astype(np.float64)
        t_quantiles /= t_quantiles[-1]
        interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)
        interp_t_values = interp_t_values.astype(olddtype)

        return interp_t_values[bin_idx].reshape(oldshape)

    @staticmethod
    def match_bands(source, template):
        """
        Splits image into bands and matches those bands to template

        :param source: image to change
        :param template: image to use as template colors
        :return: Image
        """
        bands_source = source.split()
        bands_template = template.split()
        matched_bands = []
        for x in range(0, 3):
            src = np.asarray(bands_source[x])
            tmp = np.asarray(bands_template[x])
            matched_array = FaceMasher.hist_norm(src, tmp)
            matched_bands.append(Image.fromarray(matched_array))
        bands_final = (matched_bands[0], matched_bands[1], matched_bands[2])
        merge = Image.merge("RGB", bands_final)
        return merge
